"""DiscourseTopic class."""
from .discourse_post import DiscoursePost


class DiscourseTopic:
    """Class that contains discourse topic data extracted from a JSON object."""

    def __init__(self, topic_json):
        """
        Create a topic object using a JSON object.

        Valid keys: 'id', 'title', 'slug'
        """
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
        """Display topic as invalid or by its name."""
        if self._id is None or self._name is None:
            return "Invalid Topic"
        else:
            return "Topic: " + str(self._name)

    def get_id(self):
        """Get the global discourse id of the topic."""
        return self._id

    def get_name(self):
        """Get the name of the topic."""
        return self._name

    def get_slug(self):
        """Get the readable text id for the topic."""
        return self._slug

    def add_post(self, post):
        """Add a DiscoursePost object to the topic."""
        if isinstance(post, DiscoursePost):
            self._posts.append(post)
        else:
            raise TypeError("Object of " + str(type(post)) + " is not a DiscoursePost")

    def get_posts(self):
        """Get all posts contained in the topic."""
        return self._posts
