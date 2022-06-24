from urllib import request
import json
from discourse_post import DiscoursePost

DISCOURSE_URL = (
    'https://discourse.ubuntu.com'
)

POST_JSON_URL = (
    DISCOURSE_URL + '/posts/#id.json'
)


def get_post_by_id(post_id):
    post_url = POST_JSON_URL.replace('#id', str(post_id))
    with request.urlopen(post_url) as url_data:
        json_output = json.loads(url_data.read().decode())
        return DiscoursePost(json_output)
