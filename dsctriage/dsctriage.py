#!/usr/bin/env python3

import argparse
from datetime import date, datetime, timedelta, timezone
import dscfinder

def launch():
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
    args = parser.parse_args()


if __name__ == '__main__':
    launch()
