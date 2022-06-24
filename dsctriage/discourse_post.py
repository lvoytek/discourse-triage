from datetime import datetime


class DiscoursePost:
    def __init__(self, post_json):
        self._id = post_json["id"]
        self._author_username = post_json["username"]
        self._author_name = post_json["name"]

        self._created_at = None

        try:
            self._created_at = datetime.fromisoformat(post_json["created_at"].replace('Z', '+00:00'))
        except OSError | ValueError:
            pass

        self._updated_at = None

        try:
            self._updated_at = datetime.fromisoformat(post_json["updated_at"].replace('Z', '+00:00'))
        except OSError | ValueError:
            pass

        self._data = post_json["raw"]

        self.replies = []

    def __str__(self):
        if self._id is None:
            return "Invalid Post"
        else:
            return "Post #" + str(self._id)

    def get_id(self):
        return self._id

    def get_author_username(self):
        return self._author_username

    def get_author_name(self):
        return self._author_name

    def get_creation_time(self):
        return self._created_at

    def get_update_time(self):
        return self._updated_at

    def get_data(self):
        return self._data
