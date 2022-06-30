#!/usr/bin/env python3

import argparse
import sys
from datetime import datetime, timedelta, timezone
import re
import logging
from . import dscfinder

try:
    from alive_progress import alive_bar
except ImportError:
    alive_bar = None


def parse_dates(start=None, end=None):
    """
    Validate date range and update to defaults if needed
    Default start date is 1 week ago to the day
    Default end date is today
    """
    if start is None:
        last_week = datetime.now().date() - timedelta(weeks=1)
        start = last_week.strftime('%Y-%m-%d')
    elif not re.fullmatch(r'\d{4}-\d{2}-\d{2}', start):
        raise ValueError('Cannot parse start date: ' + str(start))

    if end is None:
        today = datetime.now().date()
        end = today.strftime('%Y-%m-%d')
    elif not re.fullmatch(r'\d{4}-\d{2}-\d{2}', end):
        raise ValueError('Cannot parse end date: ' + str(end))

    return start, end


def show_header(category_name, pretty_start_date, pretty_end_date):
    """Show a dynamic header explaining results"""
    date_range_info = ('on ' + str(pretty_start_date)) \
        if pretty_start_date == pretty_end_date \
        else ('between ' + str(pretty_start_date) + ' and ' + str(pretty_end_date) + ' inclusive')

    logging.info('Discourse Comment Triage Helper')
    logging.info('Showing comments belonging to the ' + str(category_name) + ' category, updated ' + date_range_info)


def create_hyperlink(url, text):
    """Formats text into a hyperlink using ANSI escape codes."""
    return f"\u001b]8;;{url}\u001b\\{text}\u001b]8;;\u001b\\"


def print_single_comment(topic_string, post, tags, date_updated, post_url, shorten_links, show_topic_name,
                         topic_name_length=25):
    """Display info on a single post in readable format"""
    post_str = ''
    if show_topic_name:
        if len(topic_string) > topic_name_length:
            post_str += topic_string[0:topic_name_length - 1]
            post_str += '…'
        else:
            post_str += topic_string
            post_str += ' ' * (topic_name_length - len(topic_string))
    else:
        post_str += ' ' * topic_name_length

    post_str += ' - '

    base_id_str = 'id: %-6s' % str(post.get_id())

    if shorten_links:
        post_str += create_hyperlink(post_url, base_id_str)
    else:
        post_str += base_id_str

    post_str += ' %-3s ' % tags
    post_str += date_updated.strftime('%Y-%m-%d')

    if not shorten_links:
        post_str += ' [' + post_url + ']'

    print(post_str)


def print_comments(category, start, end, open_in_browser=False, shorten_links=True):
    """Display relevant posts in a readable format"""
    for topic in category.get_topics():
        post_list = []
        # Get relevant posts for a topic and add tags
        posts = topic.get_posts()
        for i in range(len(posts)):
            creation_time = posts[i].get_creation_time()
            update_time = posts[i].get_update_time()

            if (creation_time != update_time) and (start <= update_time < end):
                post_list.append((i, 'U', update_time))
            elif start <= creation_time < end:
                post_list.append((i, 'N', creation_time))

        # Display first post for a topic with topic name, then all subsequent with blank space
        for i in range(len(post_list)):
            url = dscfinder.get_post_url(topic, post_list[i][0])
            print_single_comment(topic.get_name(), posts[post_list[i][0]], post_list[i][1], post_list[i][2], url,
                                 shorten_links, i == 0)


def main(category_name, date_range=None, debug=False, progress_bar=False, open_browser=False, shorten_links=True,
         log_stream=sys.stdout):
    """Download contents of a given category, find relevant posts, print them to console"""
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

    dscfinder.add_topics_to_category(category)

    topics = category.get_topics()
    if progress_bar and alive_bar is not None:
        with alive_bar(len(topics)) as bar:
            for topic in topics:
                dscfinder.add_posts_to_topic(topic)
                bar()
    else:
        for topic in topics:
            dscfinder.add_posts_to_topic(topic)

    print_comments(category, start, end, open_browser, shorten_links)


def launch():
    """Launch discourse-triage via the command line with given arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('start_date',
                        nargs='?',
                        help='date to start finding comments ' +
                             '(e.g. 2022-04-13)')
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
    args = parser.parse_args()

    date_range = {'start': args.start_date,
                  'end': args.end_date}

    main(args.category_name, date_range, args.debug, True, args.open, not args.fullurls)
