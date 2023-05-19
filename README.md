# ![dsctriage](img/dsctriage-small.png) Discourse Triage

[![CI](https://github.com/lvoytek/discourse-triage/actions/workflows/main.yml/badge.svg)](https://github.com/lvoytek/discourse-triage/actions/workflows/main.yml)
[![dsctriage](https://snapcraft.io/dsctriage/badge.svg)](https://snapcraft.io/dsctriage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Output comments from a [Discourse](https://www.discourse.org/) server for triage. This script is used by the Ubuntu
Server team to keep up with suggested fixes and issues in the [Ubuntu Server Guide](https://ubuntu.com/server/docs), 
using [Ubuntu's Discourse site](https://discourse.ubuntu.com). It can, however, also be used to look into Discourse 
posts on any Discourse server, or other sections of Ubuntu's documentation.

The easiest way to install and keep dsctriage up to date is through snap:

```bash
sudo snap install dsctriage
```

Alternatively you can download this repository and run directly with python:

```bash
python3 -m dsctriage
```

## Usage
To run Discourse Triage with the default settings, open a terminal and enter:

    dsctriage

By default, the script will find new posts in the `Server` category that were created or updated yesterday or over the weekend and display them in the terminal. Clicking on the post ID will open a given comment in a web browser. The following arguments can be used to change functionality.

### Dates
Dates must follow the format: `%Y-%m-%d` (e.g. 2019-12-17, 2020-05-26)

#### Single Date Argument
If one date is given then posts from only that day will be found. 
For example, the following finds all posts in the `Server` category from April 27th, 2022:

    dsctriage 2022-04-27

#### Two Date Arguments
If two dates are given then all the posts created and updated on those days and between (fully inclusive) will be found. 
For example, the following, finds all posts last modified on the 10th, 11th, and 12th of September 2022:

    dsctriage 2022-09-10 2022-09-12

#### Day Name
The triage day name can also be provided to automatically extract the desired date range. For example, the following command will show all relevant comments from last Monday, which represents Tuesday triage:

    dsctriage tuesday

Running triage for Monday will show comments from last Friday and the weekend:

    dsctriage mon

### Server
To use a different Discourse server/website, use the `-s` or `--site` option, along with the desired base URL. For example,
to get yesterday's posts in the `plugin` category of [Discourse's meta site](https://meta.discourse.org/), run:

    dsctriage -s https://meta.discourse.org -c plugin

or:

    dsctriage --site https://meta.discourse.org -c plugin

### Category
If you want to find comments in a different category (see the [Ubuntu category list](https://discourse.ubuntu.com/categories)),
then you can specify it with the `-c` or `--category` option. Discourse Triage will attempt to match the name with an
existing category, case-insensitive. For example, to get comments from yesterday or over the weekend in the `Desktop` category, run
either:

    dsctriage -c desktop

or:

    dsctriage --category desktop

### Print full urls
By default, post IDs can be clicked to open in a browser. However, if your terminal does not support the hyperlink
format, or you just want the urls in plaintext you can use the `--fullurls` argument. This will print the url to the
post at the end of each line. Run the following command to get the posts from yesterday or over the weekend with their urls:

    dsctriage --fullurls

### Open in web browser
If you want all posts found to be shown in a web browser, then specify the `-o` or `--open` argument. Once the posts are
found, they will then be opened in your default browser in their own tabs. Specify the argument with either:
    
    dsctriage -o

or:
    
    dsctriage --open

### Add to backlog
To add a specific post or comment to the backlog, a formatted line of text can be printed with the `-b` or `--backlog`
argument. This text can then be copied to the backlog to be managed later. The following commands will show the post
with the ID 14159:

    dsctriage -b 14159

or:

    dsctriage --backlog 14159

### Set default category and server
To update the Discourse server and category used by default, add the `--set-defaults` argument during a dsctriage run
against them. Future runs will no longer need them to be specified each time. For example, the following will run
dsctriage and set the default category to `announcements` in the Discourse meta site: 

    dsctriage -s https://meta.discourse.org -c announcements --set-defaults

## Configuration
Alongside the `--set-defaults` argument shown above, Discourse Triage can be configured the `dsctriage.conf` file. This
can be found in `/snap/dsctriage/etc/` when using the snap, or can be added to `/etc` when running with `python3 -m`.

### Usage
The `dsctriage.conf` file works as a standard config file, where options are set in the `[dsctriage]` section using a
`=`. Here is an example of a valid `dsctriage.conf`:

    [dsctriage]
    category = doc
    site = https://forum.snapcraft.io
    progress_bar = True
    shorten_links = True

### Options
The following options can be modified in the config file:

* `category`
    - The Discourse category to look at, initially defaults to `Server`
* `site`
    - The Discourse site URL to look at, initially defaults to `https://discourse.ubuntu.com`
* `progress_bar`
    - Whether to show the progress bar when running dsctriage, defaults to `True`
* `shorten_links`
    - Whether to show links as hyperlinks in the post number, or print them fully. Defaults to `True`, making them
    hyperlinks.
