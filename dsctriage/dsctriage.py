#!/usr/bin/env python3
"""Discourse Triage frontend."""

import argparse
import sys
from enum import Enum
from datetime import datetime, timedelta, timezone
import time
import re
import logging
import webbrowser
from . import dscfinder

try:
    from alive_progress import alive_bar
except ImportError:
    alive_bar = None


class PostStatus(Enum):
    """Post update status enum."""

    UNCHANGED = 0
    NEW = 1
    UPDATED = 2


class PostWithMetadata:
    """A discourse post with additional metadata about its replies, url, and update date."""

    def __init__(self, post, status, url, update_date=None):
        """Combine a post with status, url, and update date metadata."""
        self.post = post
        self.status = status
        self.url = url
        self.update_date = update_date
        self.contains_relevant_posts = False
        self.replies = []

    def __str__(self):
        """Display post id and metadata."""
        meta_tags = ''
        if self.contains_relevant_posts:
            meta_tags += 'r'
        return f'{str(self.post)}: {("unchanged", "new", "updated")[self.status.value]} - {meta_tags}'

    def add_reply(self, meta_post):
        """Add a reply to the list of replies to this post."""
        self.replies.append(meta_post)


def auto_date_range(keyword, today=None):
    """Given a "day of week" keyword, calculate the inclusive date range.

    Work out what date range the user "means" based on the Server Team's bug
    triage process that names the day the triage is expected to be done.

    Examples: "Monday triage" means the range covering the previous Friday,
    Saturday and Sunday; "Tuesday triage" means the previous Monday only.

    :param str keyword: what the user wants in the form of the name of a day of
        the week
    :param datetime.date today: calculations are made relative to the current
        date. Can be overridden with this parameter for tests. Defaults to the
        current day
    :rtype: tuple(datetime.date, datetime.date)
    """
    triage_day = today or datetime.now().date()
    triage_found = False

    for _ in range(7):
        triage_day -= timedelta(days=1)

        if keyword.lower() in (datetime.strftime(triage_day, "%A").lower(),
                               datetime.strftime(triage_day, "%a").lower()):
            triage_found = True
            break

    if not triage_found:
        raise ValueError("Invalid day name")

    if triage_day.weekday() == 0:
        # The day is Monday, return start of Friday and end of Sunday
        return triage_day - timedelta(days=3), triage_day - timedelta(days=1)
    if triage_day.weekday() < 5:
        # Normal weekday triage, return the previous day for start and end
        return triage_day - timedelta(days=1), triage_day - timedelta(days=1)

    # Otherwise weekend was specified, no triage to do
    raise ValueError("No triage range is specified for weekday triage")


def parse_dates(start=None, end=None):
    """
    Validate date range and update to defaults if needed.

    Default start date is yesterday or last friday if today is monday.
    Default end date is yesterday.
    """
    yesterday = datetime.now().date() - timedelta(days=1)

    if start is None:
        if yesterday.weekday() != 6:
            start = yesterday.strftime('%Y-%m-%d')
        else:
            start = (yesterday - timedelta(days=2)).strftime('%Y-%m-%d')
    elif not re.fullmatch(r'\d{4}-\d{2}-\d{2}', start):
        try:
            start_date, end_date = auto_date_range(start)
            start = start_date.strftime('%Y-%m-%d')
            end = end_date.strftime('%Y-%m-%d')
        except ValueError as error:
            raise ValueError(f"Cannot parse date: {start}") from error

    if end is None:
        end = yesterday.strftime('%Y-%m-%d')
    elif not re.fullmatch(r'\d{4}-\d{2}-\d{2}', end):
        raise ValueError(f"Cannot parse end date: {str(end)}")

    return start, end


def show_header(category_name, pretty_start_date, pretty_end_date):
    """Show a dynamic header explaining results."""
    date_range_info = ('on ' + str(pretty_start_date)) \
        if pretty_start_date == pretty_end_date \
        else ('between ' + str(pretty_start_date) + ' and ' + str(pretty_end_date) + ' inclusive')

    logging.info('Discourse Comment Triage Helper')
    logging.info('Showing comments belonging to the %s category, updated %s', str(category_name), date_range_info)


def create_hyperlink(url, text):
    """Format text into a hyperlink using ANSI escape codes."""
    return f"\u001b]8;;{url}\u001b\\{text}\u001b]8;;\u001b\\"


def set_relevant_post_metadata(post_with_meta):
    """Recursively check if a post or its replies contain updates and mark its metadata accordingly."""
    is_relevant = False

    for reply in post_with_meta.replies:
        is_relevant = is_relevant or set_relevant_post_metadata(reply)

    is_relevant = is_relevant or (post_with_meta.status != PostStatus.UNCHANGED)
    post_with_meta.contains_relevant_posts = is_relevant

    return is_relevant


def print_single_comment(post, status, date_updated, post_url, shorten_links):
    """Display info on a single post in readable format."""
    status_str = ''
    if status == PostStatus.UPDATED:
        status_str = '*'
    elif status == PostStatus.NEW:
        status_str = '+'

    base_id_str = str(post.get_id())
    url_str = ''

    if shorten_links:
        base_id_str = create_hyperlink(post_url, base_id_str)
    else:
        url_str = f'({post_url})'

    date_str = '' if date_updated is None else f', {date_updated.strftime("%Y-%m-%d")}'

    post_str = f'{status_str}{base_id_str} [{dscfinder.create_author_name_str(post)}{date_str}] {url_str}'

    print(post_str)


# pylint: disable=too-many-arguments
def print_topic_post(topic, status, date_updated, author, editor, shorten_links, topic_name_length=25):
    """Display a topic's name and recent update information if relevant."""
    topic_string = topic.get_name()
    topic_url = dscfinder.get_topic_url(topic)

    status_str = ''
    if status == PostStatus.UPDATED:
        status_str = '*'
    elif status == PostStatus.NEW:
        status_str = '+'
    else:
        topic_name_length += 1

    if len(topic_string) > topic_name_length:
        topic_string = topic_string[0:topic_name_length - 1] + '…'

        if shorten_links:
            topic_string = create_hyperlink(topic_url, topic_string)
    else:
        if shorten_links:
            topic_string = create_hyperlink(topic_url, topic_string)
        topic_string += ' ' * (topic_name_length - len(topic_string))

    date_str = '' if date_updated is None else f', {date_updated.strftime("%Y-%m-%d")}'
    url_str = '' if shorten_links else f'({topic_url})'

    post_str = f'{status_str}{topic_string} [{author if editor is None else editor}{date_str}] {url_str}'

    print(post_str)


def print_comment_chain(post_with_meta, shorten_links, chain_list):
    """Display a chain of comments recursively."""
    if post_with_meta.contains_relevant_posts:
        if len(chain_list) > 0:
            indent_str = chain_list[0]
            for indent in chain_list[1:]:
                indent_str += '  ' + indent
            print(indent_str, end='─ ')
        print_single_comment(post_with_meta.post, post_with_meta.status, post_with_meta.update_date, post_with_meta.url,
                             shorten_links)

        # find all relevant replies and add to list
        relevant_replies = []
        for reply in post_with_meta.replies:
            if reply.contains_relevant_posts:
                relevant_replies.append(reply)

        if len(relevant_replies) > 0:
            if chain_list[-1] == '├':
                chain_list[-1] = '│'
            elif chain_list[-1] == '└':
                chain_list[-1] = ' '

            chain_list.append('├')

            # iterate through relevant replies
            for reply in relevant_replies[:-1]:
                print_comment_chain(reply, shorten_links, chain_list)

            chain_list[-1] = '└'
            print_comment_chain(relevant_replies[-1], shorten_links, chain_list)

            chain_list.pop()


def print_comments_within_topic(topic, post_metadata_list, shorten_links):
    """Display a topic and its relevant comments, if any."""
    # start by finding the main topic post and removing unnecessary branches by iterating over a copy of the list
    main_topic_post = None

    for post_with_meta in list(post_metadata_list):
        if post_with_meta.post.is_main_post_for_topic():
            main_topic_post = post_with_meta
        elif not post_with_meta.contains_relevant_posts:
            post_metadata_list.remove(post_with_meta)

    if main_topic_post is not None:
        main_post_author = dscfinder.create_author_name_str(main_topic_post.post)
        main_post_editor = None

        if main_topic_post.status == PostStatus.UPDATED:
            main_post_editor = dscfinder.create_editor_name_str(main_topic_post.post)

        print_topic_post(topic, main_topic_post.status, main_topic_post.update_date, main_post_author, main_post_editor,
                         shorten_links)
        post_metadata_list.remove(main_topic_post)
    else:
        print_topic_post(topic, PostStatus.UNCHANGED, None, None, shorten_links)

    # print all additional comments that have either been updated or contain updated replies
    for post_with_meta in post_metadata_list[:-1]:
        print_comment_chain(post_with_meta, shorten_links, ['├'])

    if len(post_metadata_list) > 0:
        print_comment_chain(post_metadata_list[-1], shorten_links, ['└'])


def create_post_with_metadata(post, start, end, url):
    """Add metadata to a post based on whether its creation or update time is relevant."""
    creation_time = post.get_creation_time()
    update_time = post.get_update_time()

    if (creation_time != update_time) and (start <= update_time < end):
        return PostWithMetadata(post, PostStatus.UPDATED, url, update_time)

    if start <= creation_time < end:
        return PostWithMetadata(post, PostStatus.NEW, url, creation_time)

    return PostWithMetadata(post, PostStatus.UNCHANGED, url)


def get_post_with_metadata_from_post_id(post_id, post_metadata_list):
    """Find a post in a list of posts with metadata based on its id, return None if it does not exist."""
    if post_id is not None:
        for post_with_meta in post_metadata_list:
            if post_with_meta.post.get_post_number() == post_id:
                return post_with_meta

    return None


def print_comments(category, start, end, open_in_browser=False, shorten_links=True):
    """Display relevant posts in a readable format."""
    initial_browser_open = True

    for topic in category.get_topics():
        print_topic = False
        post_metadata_list = []
        # Get relevant posts for a topic and add metadata
        for i, post in enumerate(topic.get_posts()):
            new_meta_post = create_post_with_metadata(post, start, end, dscfinder.get_post_url(topic, i))
            post_metadata_list.append(new_meta_post)

            if new_meta_post.status != PostStatus.UNCHANGED:
                print_topic = True

        # organize reply structure, remove replies from list, and open in browser if requested
        final_meta_post_list = []
        for post_item in post_metadata_list:
            replied_to_post = get_post_with_metadata_from_post_id(post_item.post.get_reply_to_number(),
                                                                  post_metadata_list)

            # post is not a reply or is a reply to the main topic, add to top level to recurse through
            if replied_to_post is None or replied_to_post.post.is_main_post_for_topic():
                final_meta_post_list.append(post_item)

            # Add this post as a reply to the found reply-to post
            if replied_to_post is not None:
                replied_to_post.add_reply(post_item)

            # open in browser if needed
            if post_item.status != PostStatus.UNCHANGED and open_in_browser:
                if initial_browser_open:
                    initial_browser_open = False
                    webbrowser.open(post_item.url)
                    time.sleep(5)
                else:
                    webbrowser.open_new_tab(post_item.url)
                    time.sleep(1.2)

        for post_item in post_metadata_list:
            set_relevant_post_metadata(post_item)

        # print topic if it contains any updates
        if print_topic:
            print_comments_within_topic(topic, final_meta_post_list, shorten_links)


def print_post_in_backlog_format(post_id):
    """Print a Discourse comment to be copied to the backlog."""
    backlog_post = dscfinder.get_post_by_id(post_id)

    if not backlog_post:
        print(f"No post found with id {post_id}")
    else:
        print_single_comment(backlog_post, PostStatus.UNCHANGED, backlog_post.get_update_time(),
                             dscfinder.get_post_url_without_topic(backlog_post), False)


def main(category_name, date_range=None, debug=False, progress_bar=False, open_browser=False, shorten_links=True,
         log_stream=sys.stdout):
    """Download contents of a given category, find relevant posts, print them to console."""
    category = dscfinder.get_category_by_name(category_name)

    if category is None:
        print("Unable to find category: " + str(category_name))
        return

    logging.basicConfig(stream=log_stream, format='%(message)s',
                        level=logging.DEBUG if debug else logging.INFO)

    date_range['start'], date_range['end'] = parse_dates(date_range['start'], date_range['end'])
    start = datetime.strptime(date_range['start'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
    end = datetime.strptime(date_range['end'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
    pretty_start = start.strftime('%Y-%m-%d (%A)')
    pretty_end = end.strftime('%Y-%m-%d (%A)')
    end += timedelta(days=1)

    show_header(category_name, pretty_start, pretty_end)

    dscfinder.add_topics_to_category(category, start)

    topics = category.get_topics()
    if progress_bar and alive_bar is not None:
        with alive_bar(len(topics)) as bar_view:
            for topic in topics:
                dscfinder.add_posts_to_topic(topic)
                bar_view()
    else:
        for topic in topics:
            dscfinder.add_posts_to_topic(topic)

    print_comments(category, start, end, open_browser, shorten_links)


def launch():
    """Launch discourse-triage via the command line with given arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('start_date',
                        nargs='?',
                        help='date or day name to start finding comments ' +
                             '(e.g. 2022-04-13, monday, Thu)')
    parser.add_argument('end_date',
                        nargs='?',
                        help='date to end finding comments (inclusive) ' +
                             '(e.g. 2022-04-27)')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='debug output')
    parser.add_argument('-o', '--open', action='store_const',
                        const=1, default=0,
                        help='open comments in web browser')
    parser.add_argument('--fullurls', default=False, action='store_true',
                        help='show full URLs instead of shortcuts')
    parser.add_argument('-c', '--category', dest='category_name', default='Server',
                        help='The discourse category to find comments from')
    parser.add_argument('-b', '--backlog', dest='backlog_post_id',
                        help='Display a post of a given ID in a standard backlog format')
    args = parser.parse_args()

    date_range = {'start': args.start_date,
                  'end': args.end_date}

    if args.backlog_post_id:
        print_post_in_backlog_format(args.backlog_post_id)
    else:
        main(args.category_name, date_range, args.debug, True, args.open, not args.fullurls)
