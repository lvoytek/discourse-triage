from urllib import request
from urllib.error import HTTPError
import json
from discourse_post import DiscoursePost
from discourse_category import DiscourseCategory
from discourse_topic import DiscourseTopic

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
    post_url = POST_JSON_URL.replace('#id', str(post_id))

    try:
        with request.urlopen(post_url) as url_data:
            json_output = json.loads(url_data.read().decode())
            return DiscoursePost(json_output)
    except HTTPError:
        return None


def get_category_by_id(category_id):
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
    try:
        with request.urlopen(CATEGORY_LIST_JSON_URL) as url_data:
            json_output = json.loads(url_data.read().decode())
            if "category_list" in json_output and "categories" in json_output["category_list"]:
                for category in json_output["category_list"]["categories"]:
                    if category["name"] == category_name:
                        return DiscourseCategory(category)
    except HTTPError:
        pass

    return None


def add_posts_to_topic(topic):
    topic_url = TOPIC_POST_LIST_JSON_URL.replace('#id', str(topic.get_id()))

    try:
        with request.urlopen(topic_url) as url_data:
            json_output = json.loads(url_data.read().decode())
            if "post_stream" in json_output and "posts" in json_output["post_stream"]:
                for post in json_output["post_stream"]["posts"]:
                    new_post = DiscoursePost(post)

                    if new_post is not None:
                        topic.add_post(new_post)

    except HTTPError:
        pass


def add_topics_to_category(category):
    category_url = CATEGORY_TOPIC_LIST_JSON_URL.replace('#id', str(category.get_id()))

    try:
        with request.urlopen(category_url) as url_data:
            json_output = json.loads(url_data.read().decode())
            if "topic_list" in json_output and "topics" in json_output["topic_list"]:
                for topic in json_output["topic_list"]["topics"]:
                    new_topic = DiscourseTopic(topic)
                    add_posts_to_topic(new_topic)

                    if new_topic is not None:
                        category.add_topic(new_topic)

    except HTTPError:
        pass
