"""DiscourseCategory class."""
from .discourse_topic import DiscourseTopic


class DiscourseCategory:
    """Class that contains discourse category data extracted from a JSON object."""

    def __init__(self, category_json):
        """
        Create a topic object using a JSON object.

        Valid keys: 'id', 'name', 'description_text'
        """
        self._id = None
        self._name = None
        self._description = None

        if "id" in category_json:
            self._id = category_json["id"]

        if "name" in category_json:
            self._name = category_json["name"]

        if "description_text" in category_json:
            self._description = category_json["description_text"]

        self._topics = []

    def __str__(self):
        """Display category as invalid or by its name."""
        if self._id is None or self._name is None:
            return "Invalid Category"
        else:
            return "Category: " + str(self._name)

    def get_id(self):
        """Get the global discourse id for the category."""
        return self._id

    def get_name(self):
        """Get the name of the category."""
        return self._name

    def get_description(self):
        """Get the short description of the category."""
        return self._description

    def add_topic(self, topic):
        """Add a DiscourseTopic object to the category."""
        if isinstance(topic, DiscourseTopic):
            self._topics.append(topic)
        else:
            raise TypeError("Object of " + str(type(topic)) + " is not a DiscourseTopic")

    def get_topics(self):
        """Get all topics contained in the category."""
        return self._topics
