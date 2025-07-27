# Changelog

All notable changes to this project are documented in this file.

## [0.10.0] - 2024-12-30

### Changed
- Updates bulma style.css to v1.0.4
- Updates poetry dependencies
- Drops Python 3.7, 3.8, 3.9 support
- Adds Django 4/5 support
- Updates dependencies and workflows
- Removes legacy version check
- Fixed is_radio filter for django 4.0

### Updated
- Replace node-sass with dart-sass (official version used by bulma)
- Update Bulma along with all dependencies

## [0.8.3] - 2021-10-21

### Fixed
- Updates outdated CircleCI Docker images
- Fixes failing CircleCI Docker images

### Updated
- Updates bulma to 0.9.3

## [0.8.2] - 2021-03-24

### Changed
- Removes upper bound for Django version
- Adds python-3.9 test environment

## [0.8.1] - 2020-08-31

### Fixed
- Adds label 'for' attribute for form inputs with auto ID's

### Changed
- Allow Django 3.1

## [0.8.0] - 2020-07-20

### Updated
- Upgrades Bulma.css to 0.9.0
- Updates CircleCI python containers

### Fixed
- Fix help text css class for multiple checkbox field

## [0.7.1] - 2020-05-11

### Updated
- Upgrades bulma to 0.8.2
- Updates dependencies

### Added
- Adds custom field_template feature

### Fixed
- Fixes failing tests
- Replaces bulma filter with tag

## [0.6.0] - 2019-08-20

### Changed
- Moves to poetry
- Upgrades to bulma 0.7.5

### Improved
- Improves package config
- Adds command output tests
- Updates assets

### Added
- Adds template tests

## [0.5.7] - 2019-07-15

### Changed
- Moves to poetry
- Upgrades to bulma 0.7.5

## [0.5.6] - 2019-03-18

### Removed
- Removes font awesome from the repo
- Replaces font awesome with CDN link

## [0.5.5] - 2019-01-28

### Fixed
- Fixes version in package.json
- Fixes linebreaks in allauth's account/* templates

### Updated
- Updates requirements.txt

## [0.5.4] - 2018-12-17

### Updated
- Updates bulma dependency to 0.7.4

## [0.5.3] - 2018-10-30

### Updated
- Upgrades bulma css to 0.7.2

### Fixed
- Improves the way Boundfield is detected

## [0.5.1] - 2018-06-10

### Updated
- Update to bulma 0.7.1

### Changed
- Use setuptools_scm

## [0.5.0] - 2018-04-16

### Updated
- Updates to bulma 0.7.0

### Fixed
- Fix code typo in README

## [0.4.0] - 2018-02-28

### Added
- Adds .is-danger to invalid form inputs
- Adds more examples
- Adds basic file input

### Updated
- Updates demo examples with allauth login / signup links

## [0.3.4] - 2018-01-30

### Updated
- Updates bulma to 0.6.2

### Fixed
- Fix TypeError (convert int to str)

## [0.3.3] - 2017-12-18

### Added
- Adds bulma_message_tag filter that converts Django 'error' tag to Bulma 'danger'

## [0.3.2] - 2017-11-20

### Added
- Adds support for multiple select fields

### Changed
- Enters beta phase

## [0.3.1] - 2017-11-06

### Updated
- Updates bulma to 0.6.1

### Added
- Adds support for forms.URLInput and forms.NumberInput

## [0.3.0] - 2017-10-18

### Changed
- Moved bulma source to dependencies installable via NPM
- Moves fontawesome under bulma static namespace

### Added
- Added logo
- Add FontAwesome, make base template mobile-friendly

## [0.2.0] - 2017-10-12

### Added
- Adds manage.py bulma command
- Adds copy_bulma_static_into_project command

### Changed
- Reorganizes templates
- Reorganizes static files

### Fixed
- Fixes management commands

## [0.1.0] - 2017-10-11

### Added
- Initial PYPI release
- Adds example app

### Fixed
- Fixes pagination template
- Fixes 'TypeError context must be a dict rather than Context'

### Changed
- Cleans up base template
- Gets rid of site_base.html

## [0.0.3] - 2017-10-05

### Updated
- Upgrades Bulma to 0.6.0

### Added
- Adds basic documentation in README

## [0.0.2] - 2017-09-29

### Fixed
- Fixes pagination template
- Fixes 'TypeError context must be a dict rather than Context'

### Added
- Adds PYPI config
- Adds customizable style.sass
- Adds bulma markup

## [0.0.1] - 2017-09-28

### Added
- Initial commit
- Basic project structure