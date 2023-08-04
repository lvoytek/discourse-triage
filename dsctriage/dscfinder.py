"""Discourse API handler module."""
from urllib import request
from urllib.error import HTTPError
import json
from .discourse_post import DiscoursePost
from .discourse_topic import DiscourseTopic
from .discourse_category import DiscourseCategory

DEFAULT_DISCOURSE_URL = "https://discourse.ubuntu.com"

POST_JSON_URL = "#url/posts/#id.json"

POST_LATEST_EDIT_JSON_URL = "#url/posts/#id/revisions/latest.json"

CATEGORY_JSON_URL = "#url/c/#id/show.json"

CATEGORY_TOPIC_LIST_JSON_URL = "#url/c/#id.json"

CATEGORY_LIST_JSON_URL = "#url/categories.json?include_subcategories=true"

TOPIC_POST_LIST_JSON_URL = "#url/t/#id.json"

TOPIC_POST_BATCH_JSON_URL = "#url/t/#id/posts.json"

USER_JSON_URL = "#url/u/#id.json"


def create_url(template, id_var, site=None):
    """
    Create a URL string from an above template, a website base name, and id variable.

    If the site is None then use the default.
    """
    return template.replace("#url", str(DEFAULT_DISCOURSE_URL if site is None else site)).replace("#id", str(id_var))


def extract_posts_from_json_post_stream(json_output):
    """
    Extract all available posts from json in a post stream and return them as a list of DiscoursePost objects.

    Returns an empty array if json is invalid or contains no posts
    """
    posts = []
    if "post_stream" in json_output and "posts" in json_output["post_stream"]:
        for post in json_output["post_stream"]["posts"]:
            new_post = DiscoursePost(post)
            if new_post is not None:
                posts.append(new_post)

    return posts


def get_post_by_id(post_id, site=None):
    """
    Download post data for a given id and return it as a DiscoursePost object.

    Returns None if download fails or id is invalid.
    """
    post_url = create_url(POST_JSON_URL, post_id, site)

    try:
        with request.urlopen(post_url) as url_data:
            json_output = json.loads(url_data.read().decode())
        return DiscoursePost(json_output)
    except HTTPError:
        return None


def get_batch_of_posts_by_id(topic_id, post_ids, site=None):
    """
    Download post data for a list of given post ids in a topic and return it as a list of DiscoursePost objects.

    Invalid post ids are ignored
    Returns None if download fails, or an emtpy list if there are no valid ids
    """
    if post_ids is None or len(post_ids) == 0:
        return []

    posts_url = create_url(TOPIC_POST_BATCH_JSON_URL, topic_id, site)

    # append post ids to the url through params with the format post_ids[]=<id>
    posts_url += f"?post_ids[]={post_ids[0]}"
    for post_id in post_ids[1::]:
        posts_url += f"&post_ids[]={post_id}"

    try:
        with request.urlopen(posts_url) as url_data:
            json_output = json.loads(url_data.read().decode())

        return extract_posts_from_json_post_stream(json_output)

    except HTTPError:
        return None


def get_category_by_id(category_id, site=None):
    """
    Download category data for a given id and return it as a DiscourseCategory object.

    Returns None if download fails or id is invalid.
    """
    category_url = create_url(CATEGORY_JSON_URL, category_id, site)

    try:
        with request.urlopen(category_url) as url_data:
            json_output = json.loads(url_data.read().decode())

        if "category" in json_output:
            return DiscourseCategory(json_output["category"])
    except HTTPError:
        pass

    return None


def get_category_by_name(category_name, site=None):
    """
    Download category data for a given category or category/subcategory/... name (case-insensitive).

    Returns result as a DiscourseCategory object or None if download fails or name is invalid.
    """
    category_nav = category_name.split("/")
    final_category = None

    try:
        with request.urlopen(create_url(CATEGORY_LIST_JSON_URL, "", site)) as url_data:
            json_output = json.loads(url_data.read().decode())
        if "category_list" in json_output and "categories" in json_output["category_list"]:
            for category in json_output["category_list"]["categories"]:
                if category["name"].lower() == category_nav[0].lower():
                    final_category = DiscourseCategory(category)

                    # Some discourse sites fail to provide a subcategory list, check subcategory ids in this case
                    if "subcategory_list" not in category and "subcategory_ids" in category:
                        add_subcategories_to_category_by_ids(final_category, category["subcategory_ids"], site)

    except HTTPError:
        pass

    for i in range(1, len(category_nav)):
        if final_category:
            final_category = final_category.get_subcategory_by_name(category_nav[i])
        else:
            break

    return final_category


def add_subcategories_to_category_by_ids(category, subcategory_ids, site=None):
    """Add subcategories with ids contained in an array to a parent category."""
    for subcategory_id in subcategory_ids:
        new_subcategory = get_category_by_id(subcategory_id, site)
        if new_subcategory:
            category.add_subcategory(new_subcategory)


def add_posts_to_topic(topic, site=None):
    """Download data for all posts under a given topic and add them as DiscoursePosts to that topic."""
    topic_url = create_url(TOPIC_POST_LIST_JSON_URL, topic.get_id(), site)

    try:
        with request.urlopen(topic_url) as url_data:
            json_output = json.loads(url_data.read().decode())

        # get initial set of posts from the post_stream > posts section of the JSON
        for new_post in extract_posts_from_json_post_stream(json_output):
            topic.add_post(new_post)

        # not all posts always show up in the posts section, so determine which ones are missing
        posts_to_get = []
        if "post_stream" in json_output and "stream" in json_output["post_stream"]:
            for post_id in json_output["post_stream"]["stream"]:
                post_exists = False
                for post in topic.get_posts():
                    if str(post_id) == str(post.get_id()):
                        post_exists = True
                        break
                if not post_exists:
                    posts_to_get.append(post_id)

        # download missing posts that show up in the stream section batching requests if the chunk size is known
        chunk_size = int(json_output["chunk_size"]) if "chunk_size" in json_output else 1
        for i in range(0, len(posts_to_get), chunk_size):
            if i + chunk_size > len(posts_to_get):
                new_posts = get_batch_of_posts_by_id(topic.get_id(), posts_to_get[i::], site)
            else:
                new_posts = get_batch_of_posts_by_id(topic.get_id(), posts_to_get[i : i + chunk_size], site)

            if new_posts is not None:
                for new_post in new_posts:
                    topic.add_post(new_post)

    except HTTPError:
        pass


def add_topics_to_category(category, ignore_before_date=None, site=None):
    """Download data for all topics under a given category and add them as DiscourseTopics to that category."""
    category_url = create_url(CATEGORY_TOPIC_LIST_JSON_URL, category.get_id(), site)

    try:
        with request.urlopen(category_url) as url_data:
            json_output = json.loads(url_data.read().decode())
        if "topic_list" in json_output and "topics" in json_output["topic_list"]:
            for topic in json_output["topic_list"]["topics"]:
                new_topic = DiscourseTopic(topic)

                update_time = None if new_topic is None else new_topic.get_latest_update_time()
                accept_date = ignore_before_date is None or update_time is None or update_time >= ignore_before_date

                if new_topic is not None and accept_date:
                    category.add_topic(new_topic)

    except HTTPError:
        pass


def get_topic_url(topic, site=None):
    """Get the human-readable site url of a given topic."""
    return f"{DEFAULT_DISCOURSE_URL if site is None else site}/t/{str(topic.get_id())}"


def get_post_url_without_topic(post, site=None):
    """Get a URL shortcut to a post based on its id alone."""
    return f"{DEFAULT_DISCOURSE_URL if site is None else site}/p/{str(post.get_id())}"


def get_post_url(topic, post_index, site=None):
    """Get the human-readable site url of a post belonging to a given topic."""
    url = get_topic_url(topic, site)
    posts = topic.get_posts()

    if 0 <= post_index < len(posts):
        url += "/" + str(posts[post_index].get_post_number())

    return url


def create_author_name_str(post):
    """Create a formatted author string based on a post's original author."""
    return post.get_author_username() if post.get_author_name() in (None, "") else post.get_author_name()


def create_editor_name_str(post, site=None):
    """Create a formatted author string based on either name or username of a post's most recent editor."""
    author_name = post.get_author_username() if post.get_author_name() in (None, "") else post.get_author_name()

    if post.is_main_post_for_topic():
        revision_url = create_url(POST_LATEST_EDIT_JSON_URL, post.get_id(), site)

        try:
            with request.urlopen(revision_url) as url_data:
                json_output = json.loads(url_data.read().decode())
            if "username" in json_output:
                author_name = json_output["username"]

                user_url = create_url(USER_JSON_URL, json_output["username"])
            with request.urlopen(user_url) as user_url_data:
                user_json_output = json.loads(user_url_data.read().decode())

            if "user" in user_json_output and "name" in user_json_output["user"]:
                author_name = user_json_output["user"]["name"]

        except HTTPError:
            pass

    return author_name
