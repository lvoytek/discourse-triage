from discourse_post import DiscoursePost


class DiscourseTopic:
    def __init__(self, topic_json):
        self._id = None
        self._name = None
        self._slug = None

        if "id" in topic_json:
            self._id = topic_json["id"]

        if "title" in topic_json:
            self._name = topic_json["title"]

        if "slug" in topic_json:
            self._slug = topic_json["slug"]

        self._posts = []

    def __str__(self):
        if self._id is None or self._name is None:
            return "Invalid Topic"
        else:
            return "Topic: " + str(self._name)

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_slug(self):
        return self._slug

    def add_post(self, post):
        if isinstance(post, DiscoursePost):
            self._posts.append(post)
        else:
            raise TypeError("Object of " + type(post) + " is not a DiscoursePost")

    def get_posts(self):
        return self._posts
