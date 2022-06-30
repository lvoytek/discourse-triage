#!/usr/bin/env python3

import argparse
import sys
from datetime import datetime, timedelta
import re
import logging
from . import dscfinder


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


def main(category_name, date_range=None, debug=False, open_browser=False, shorten_links=True, log_stream=sys.stdout):
    """Download contents of a given category, find relevant posts, print them to console"""
    category = dscfinder.get_category_by_name(category_name)

    if category is None:
        print("Unable to find category: " + str(category_name))
        return

    logging.basicConfig(stream=log_stream, format='%(message)s',
                        level=logging.DEBUG if debug else logging.INFO)

    date_range['start'], date_range['end'] = parse_dates(date_range['start'], date_range['end'])
    start = datetime.strptime(date_range['start'], '%Y-%m-%d')
    end = datetime.strptime(date_range['end'], '%Y-%m-%d')
    pretty_start = start.strftime('%Y-%m-%d (%A)')
    pretty_end = end.strftime('%Y-%m-%d (%A)')
    end += timedelta(days=1)

    show_header(category_name, pretty_start, pretty_end)

    dscfinder.add_topics_to_category(category)


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

    main(args.category_name, date_range, args.debug, args.open, not args.fullurls)
