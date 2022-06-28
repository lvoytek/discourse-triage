from discourse_topic import DiscourseTopic


class DiscourseCategory:
    def __init__(self, category_json):
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
        if self._id is None or self._name is None:
            return "Invalid Category"
        else:
            return "Category: " + str(self._name)

    def __iter__(self):
        return

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def add_topic(self, topic):
        if isinstance(topic, DiscourseTopic):
            self._topics.append(topic)
        else:
            raise TypeError("Object of " + type(topic) + " is not a DiscourseTopic")

    def get_topics(self):
        return self._topics