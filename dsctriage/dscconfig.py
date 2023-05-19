"""dsctriage configuration manager."""
import configparser
from pathlib import Path

default_config = {
    "dsctriage": {
        "category": "Server",
        "site": "https://discourse.ubuntu.com",
        "progress_bar": True,
        "shorten_links": True,
    }
}


def get_default_config_filename():
    """Get the default file path to get and put dsctriage.conf."""
    try:
        return f"{Path.home()}/.config/dsctriage.conf"
    except RuntimeError:
        return "/etc/dsctriage.conf"


class Config:
    """Class for interacting with a dsctriage config file."""

    def __init__(self, config_filename=None):
        """Set configuration to default then update config from aa given file if available."""
        self._config = configparser.ConfigParser()
        self._config.read_dict(default_config)

        if not config_filename:
            config_filename = get_default_config_filename()

        try:
            self._config.read(config_filename)
        except FileNotFoundError:
            pass

    def save(self, config_filename=None):
        """Save configuration to a file."""
        if not config_filename:
            config_filename = get_default_config_filename()

        Path.mkdir(Path(config_filename).parent, parents=True, exist_ok=True)

        with open(config_filename, "w", encoding="utf-8") as config_file:
            self._config.write(config_file)

    @property
    def category(self):
        """Get the value of the default Discourse category to gather data from."""
        return self._config.get("dsctriage", "category")

    @category.setter
    def category(self, value):
        """Set the default Discourse category to gather data from."""
        self._config.set("dsctriage", "category", value)

    @property
    def site(self):
        """Get the value of the default Discourse site URL to gather data from."""
        return self._config.get("dsctriage", "site")

    @site.setter
    def site(self, value):
        """Set the default Discourse site URL to gather data from."""
        self._config.set("dsctriage", "site", value)

    @property
    def progress_bar(self):
        """Get the configuration for whether to show the progress bar during download."""
        return self._config.getboolean("dsctriage", "progress_bar")

    @progress_bar.setter
    def progress_bar(self, value):
        """Set the configuration for whether to show the progress bar during download."""
        self._config.set("dsctriage", "progress_bar", value)

    @property
    def shorten_links(self):
        """Get the configuration for whether to use hyperlinks or full links in the output."""
        return self._config.getboolean("dsctriage", "shorten_links")

    @shorten_links.setter
    def shorten_links(self, value):
        """Set the configuration for whether to use hyperlinks or full links in the output."""
        self._config.set("dsctriage", "shorten_links", value)
