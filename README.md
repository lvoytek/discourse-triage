# Discourse Triage

[![CI](https://github.com/lvoytek/discourse-triage/actions/workflows/main.yml/badge.svg)](https://github.com/lvoytek/discourse-triage/actions/workflows/main.yml)
[![dsctriage](https://snapcraft.io/dsctriage/badge.svg)](https://snapcraft.io/dsctriage)

Output comments from [Ubuntu Discourse](https://discourse.ubuntu.com) for triage. This script is used by the Ubuntu
Server team to keep up with suggested fixes and issues in the [Ubuntu Server Guide](https://ubuntu.com/server/docs). It
can, however, also be used to look into Discourse posts in other sections of Ubuntu's documentation.

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

### Category
If you want to find comments in a different category (see the [category list](https://discourse.ubuntu.com/categories)),
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