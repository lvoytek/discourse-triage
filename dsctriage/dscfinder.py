"""Discourse API handler module."""
from urllib import request
from urllib.error import HTTPError
import json
from .discourse_post import DiscoursePost
from .discourse_topic import DiscourseTopic
from .discourse_category import DiscourseCategory

DISCOURSE_URL = (
    'https://discourse.ubuntu.com'
)

POST_JSON_URL = (
        DISCOURSE_URL + '/posts/#id.json'
)

CATEGORY_JSON_URL = (
        DISCOURSE_URL + '/c/#id/show.json'
)

CATEGORY_TOPIC_LIST_JSON_URL = (
        DISCOURSE_URL + '/c/#id.json'
)

CATEGORY_LIST_JSON_URL = (
        DISCOURSE_URL + '/categories.json'
)

TOPIC_POST_LIST_JSON_URL = (
        DISCOURSE_URL + '/t/#id.json'
)


def get_post_by_id(post_id):
    """
    Download post data for a given id and return it as a DiscoursePost object.

    Returns None if download fails or id is invalid.
    """
    post_url = POST_JSON_URL.replace('#id', str(post_id))

    try:
        with request.urlopen(post_url) as url_data:
            json_output = json.loads(url_data.read().decode())
            return DiscoursePost(json_output)
    except HTTPError:
        return None


def get_category_by_id(category_id):
    """
    Download category data for a given id and return it as a DiscourseCategory object.

    Returns None if download fails or id is invalid.
    """
    category_url = CATEGORY_JSON_URL.replace('#id', str(category_id))

    try:
        with request.urlopen(category_url) as url_data:
            json_output = json.loads(url_data.read().decode())

            if "category" in json_output:
                return DiscourseCategory(json_output["category"])
    except HTTPError:
        pass

    return None


def get_category_by_name(category_name):
    """
    Download category data for a given category name (case-insensitive) and return it as a DiscourseCategory object.

    Returns None if download fails or name is invalid.
    """
    try:
        with request.urlopen(CATEGORY_LIST_JSON_URL) as url_data:
            json_output = json.loads(url_data.read().decode())
            if "category_list" in json_output and "categories" in json_output["category_list"]:
                for category in json_output["category_list"]["categories"]:
                    if category["name"].lower() == category_name.lower():
                        return DiscourseCategory(category)
    except HTTPError:
        pass

    return None


def add_posts_to_topic(topic):
    """Download data for all posts under a given topic and add them as DiscoursePosts to that topic."""
    topic_url = TOPIC_POST_LIST_JSON_URL.replace('#id', str(topic.get_id()))

    try:
        with request.urlopen(topic_url) as url_data:
            json_output = json.loads(url_data.read().decode())
            # get initial set of posts from the post_stream > posts section of the JSON
            if "post_stream" in json_output and "posts" in json_output["post_stream"]:
                for post in json_output["post_stream"]["posts"]:
                    new_post = DiscoursePost(post)

                    if new_post is not None:
                        topic.add_post(new_post)

            # not all posts always show up in the posts section, so download remainder from the stream section
            if "post_stream" in json_output and "stream" in json_output["post_stream"]:
                for post_id in json_output["post_stream"]["stream"]:
                    post_exists = False
                    for post in topic.get_posts():
                        if str(post_id) == str(post.get_id()):
                            post_exists = True
                            break

                    if not post_exists:
                        new_post = get_post_by_id(post_id)
                        if new_post:
                            topic.add_post(new_post)
    except HTTPError:
        pass


def add_topics_to_category(category):
    """Download data for all topics under a given category and add them as DiscourseTopics to that category."""
    category_url = CATEGORY_TOPIC_LIST_JSON_URL.replace('#id', str(category.get_id()))

    try:
        with request.urlopen(category_url) as url_data:
            json_output = json.loads(url_data.read().decode())
            if "topic_list" in json_output and "topics" in json_output["topic_list"]:
                for topic in json_output["topic_list"]["topics"]:
                    new_topic = DiscourseTopic(topic)

                    if new_topic is not None:
                        category.add_topic(new_topic)

    except HTTPError:
        pass


def get_topic_url(topic):
    """Get the human-readable site url of a given topic."""
    return DISCOURSE_URL + "/t/" + str(topic.get_id())


def get_post_url(topic, post_index):
    """Get the human-readable site url of a post belonging to a given topic."""
    url = get_topic_url(topic)
    posts = topic.get_posts()

    if 0 <= post_index < len(posts):
        url += "/" + str(posts[post_index].get_post_number())

    return url
