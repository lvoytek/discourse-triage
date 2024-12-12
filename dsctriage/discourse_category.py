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

        self._subcategories = []
        if "subcategory_list" in category_json:
            for subcategory in category_json["subcategory_list"]:
                self.add_subcategory(DiscourseCategory(subcategory))

        self._topics = []

    def __str__(self):
        """Display category as invalid or by its name."""
        if self._id is None or self._name is None:
            return "Invalid Category"
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
            raise TypeError("Object of type " + str(type(topic)) + " is not a DiscourseTopic")

    def get_topics(self):
        """Get all topics contained in the category."""
        return self._topics

    def add_subcategory(self, subcategory):
        """Add a DiscourseCategory object as a subcategory to the category."""
        if isinstance(subcategory, DiscourseCategory):
            self._subcategories.append(subcategory)
        else:
            raise TypeError("Object of type " + str(type(subcategory)) + " is not a DiscourseCategory")

    def get_subcategories(self):
        """Get all the category's subcategories."""
        return self._subcategories

    def get_subcategory_by_id(self, subcategory_id):
        """Get a subcategory with the given id or return None if it does not exist."""
        for subcategory in self._subcategories:
            if subcategory.get_id() == subcategory_id:
                return subcategory

        return None

    def get_subcategory_by_name(self, subcategory_name):
        """Get the first subcategory with the given name or return None if it does not exist."""
        for subcategory in self._subcategories:
            if subcategory.get_name().lower() == subcategory_name.lower():
                return subcategory

        return None
