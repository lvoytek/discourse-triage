# Changelog

## Unreleased

### Changed

* Clear progress bar when download is complete for cleaner copy-paste of output
* snapcraft.yaml summary and description to better match readme

### Fixed

* Default triage range when using on Mondays to include whole weekend

## 1.4.0

Released on February 10, 2023

### Added

* Standard formatting using [black](https://github.com/psf/black)
* Changelog file
* [Logo](img/dsctriage.png) in images folder and in Readme

### Changed

* Additional post downloading through batches to increase speed
* Close requests as soon as possible
* Tox file refactoring

### Fixed

* Use pytest entry point instead of py.test in tox file

## 1.3.0

Released on December 1, 2022

### Added

* Ability to use dsctriage on other discourse websites [#2](https://github.com/lvoytek/discourse-triage/issues/2)

### Changed

* Author field of main topic post to show editor when it has been updated [#1](https://github.com/lvoytek/discourse-triage/issues/1)
* Single date argument to show updates from just that day rather than up to today [#3](https://github.com/lvoytek/discourse-triage/issues/3)

## 1.2.0

Released on November 2, 2022

### Added

* Triage parsing by name of day
* Command line option to display a post formatted for the backlog

### Changed

* Default date range to be either yesterday or over the weekend

## 1.1.0

Released on July 21, 2022

### Added

* Tree format for displaying triaged posts based on replies
* CI testing and lint checking
	- Use flake8 and pylint for format checking
    - Use pytest for unit tests
    - Added GitHub CI file
    - Added tox file

### Changed

* Reduced required number of downloads based on update times
* Author display format

### Fixed

* Missing post updates from bad metadata
* F-string formatting
* Lint issues

## 1.0.0

Released on July 1, 2022

### Added

* Initial full release including:
	- Discourse post download functionality
    - Simple frontend for displaying posts
    - Timing-based triage of posts
* Snapcraft file for building dsctriage snap
* Instructions to Readme
* Full coverage unit tests

## 0.1.0

Released on June 23, 2022.

### Added

* Initial setup of repository, containing:
	- README.md
	- LICENSE
	- .gitignore
	- setup.py
    - dsctriage.py
