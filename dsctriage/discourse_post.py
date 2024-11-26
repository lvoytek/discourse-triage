"""DiscoursePost class."""

from datetime import datetime


class DiscoursePost:
    """Class that contains discourse post data extracted from a JSON object."""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, post_json):
        """
        Create a post object using a JSON object.

        Valid keys: 'id', 'username', 'name', 'created_at', 'updated_at', 'post_number', 'raw', 'reply_count',
        'reply_to_post_number'
        """
        self._id = None
        self._author_username = None
        self._author_name = None
        self._created_at = None
        self._updated_at = None
        self._post_number = None
        self._data = None
        self._num_replies = None
        self._reply_to_number = None

        if "id" in post_json:
            self._id = post_json["id"]

        if "username" in post_json:
            self._author_username = post_json["username"]

        if "name" in post_json:
            self._author_name = post_json["name"]

        try:
            if "created_at" in post_json:
                self._created_at = datetime.fromisoformat(post_json["created_at"].replace("Z", "+00:00"))
        except (OSError, ValueError):
            pass

        try:
            if "updated_at" in post_json:
                self._updated_at = datetime.fromisoformat(post_json["updated_at"].replace("Z", "+00:00"))
        except (OSError, ValueError):
            pass

        if "post_number" in post_json:
            self._post_number = post_json["post_number"]

        if "raw" in post_json:
            self._data = post_json["raw"]

        if "reply_count" in post_json:
            self._num_replies = post_json["reply_count"]

        if "reply_to_post_number" in post_json:
            self._reply_to_number = post_json["reply_to_post_number"]

    def __str__(self):
        """Display post as invalid or by its id."""
        if self._id is None:
            return "Invalid Post"
        return "Post #" + str(self._id)

    def get_id(self):
        """Get discourse post global id."""
        return self._id

    def get_author_username(self):
        """Get the username of the post's creator."""
        return self._author_username

    def get_author_name(self):
        """Get the name of the post's creator."""
        return self._author_name

    def get_creation_time(self):
        """Get the UTC time in which the post was created."""
        return self._created_at

    def get_update_time(self):
        """Get the UTC time in which the post was last updated."""
        return self._updated_at

    def get_post_number(self):
        """Get the post's number within the topic."""
        return self._post_number

    def get_data(self):
        """Get the raw data from the post."""
        return self._data

    def get_num_replies(self):
        """Get the number of post replies to this post."""
        return self._num_replies

    def get_reply_to_number(self):
        """Get the post number that this post is a reply to if any."""
        return self._reply_to_number

    def is_main_post_for_topic(self):
        """Check if this post is the main post a given topic is about."""
        return self._post_number == 1
