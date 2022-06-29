from datetime import datetime


class DiscoursePost:
    def __init__(self, post_json):
        self._id = None
        self._author_username = None
        self._author_name = None
        self._created_at = None
        self._updated_at = None
        self._post_number = None
        self._data = None

        if "id" in post_json:
            self._id = post_json["id"]

        if "username" in post_json:
            self._author_username = post_json["username"]

        if "name" in post_json:
            self._author_name = post_json["name"]

        try:
            if "created_at" in post_json:
                self._created_at = datetime.fromisoformat(post_json["created_at"].replace('Z', '+00:00'))
        except (OSError, ValueError):
            pass

        try:
            if "updated_at" in post_json:
                self._updated_at = datetime.fromisoformat(post_json["updated_at"].replace('Z', '+00:00'))
        except (OSError,  ValueError):
            pass

        if "post_number" in post_json:
            self._post_number = post_json["post_number"]

        if "raw" in post_json:
            self._data = post_json["raw"]

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

    def get_post_number(self):
        return self._post_number

    def get_data(self):
        return self._data
