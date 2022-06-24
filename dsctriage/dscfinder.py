from urllib import request
from urllib.error import HTTPError
import json
from discourse_post import DiscoursePost
from discourse_category import DiscourseCategory

DISCOURSE_URL = (
    'https://discourse.ubuntu.com'
)

POST_JSON_URL = (
        DISCOURSE_URL + '/posts/#id.json'
)

CATEGORY_JSON_URL = (
        DISCOURSE_URL + '/c/#id/show.json'
)

CATEGORY_LIST_JSON_URL = (
        DISCOURSE_URL + '/categories.json'
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
