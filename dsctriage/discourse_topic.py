"""DiscourseTopic class."""

from datetime import datetime
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
        self._latest_update_time = None

        if "id" in topic_json:
            self._id = topic_json["id"]

        if "title" in topic_json:
            self._name = topic_json["title"]

        if "slug" in topic_json:
            self._slug = topic_json["slug"]

        try:
            if "bumped" in topic_json and topic_json["bumped"] and "bumped_at" in topic_json:
                self._latest_update_time = datetime.fromisoformat(topic_json["bumped_at"].replace("Z", "+00:00"))

            if "last_posted_at" in topic_json:
                last_posted_at = datetime.fromisoformat(topic_json["last_posted_at"].replace("Z", "+00:00"))
                self._latest_update_time = max(self._latest_update_time, last_posted_at)

        except (OSError, ValueError):
            pass

        self._tags = []
        if "tags" in topic_json:
            for tag in topic_json["tags"]:
                self._tags.append(str(tag))

        self._posts = []

    def __str__(self):
        """Display topic as invalid or by its name."""
        if self._id is None or self._name is None:
            return "Invalid Topic"
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

    def get_latest_update_time(self):
        """Get the most recent update time as a DateTime."""
        return self._latest_update_time

    def get_tags(self):
        """Get the list of tags associated with the topic."""
        return self._tags

    def has_tag(self, tag_name):
        """Check if the topic has the given tag."""
        for contained_tag_name in self._tags:
            if tag_name == contained_tag_name:
                return True

        return False
