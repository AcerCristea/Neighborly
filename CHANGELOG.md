# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres mostly to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
There may be minor-version updates that contain breaking changes, but do not warrant
incrementing to a completely new version number.

## [0.9.5]

- The entire package has been restructures as some modules have moved
  out of the core module and into other packages
- Added `components` package to manage all the various built-in
  components
- Compresses the LifeEvent API to use a single class
  and moved support for queries or role lists to utility functions
- Removed `pandas` as a dependency for queries because it was too
  slow
- Separated out the default plugins into separate modules
- Revised the YAML loading API
- Revised the archetype authoring pipeline, introducing new config
  objects that hold metadata. This replaces the archetype functions
  that would have normally supplied this data.
- System priority constants are now defined using negative numbers
  this allows us to have a wider range of values for priorities below
  the built-in systems
- The `engine.py` module now handles more of the authored content
  such as archetypes
- Status system creates child gameobjects that may have time-released
  effects on the simulation state
- Consolidated redundant components such as `Gender` into a single
  component with an enum value

## [0.9.4]

**0.9.4 is not compatible with 0.9.3**

### Added

- `Building` class to identify when a business currently exists within the town vs.
  when it is archived within the ECS for story sifting.
- Systems to update business components when they are pending opening, open for business, and closed for business and
  awaiting demolition.
- New status components to identify Businesses at different phases in their lifecycle:
  `ClosedForBusiness`, `OpenForBusiness`, `PendingOpening`
- New PyGame UI elements for displaying information about a GameObject
- Strings may be used as world seeds
- `CHANGELOG.md` file

### Updated

- PyGame sample to use the new API
- Docstrings for `Simulation` and `SimulationBuilder` classes
- `SimulationBuilder` class
- Moved isort configuration to `pyproject.toml`

### Removed

- Jupyter notebook and pygame samples
- samples category from dependencies within `setup.cfg`
- `events`, `town`, `land grid`, and `relationships` fields from `NeighborlyJsonExporter`.
  These are duplicated when serializing the resources.
- `SimulationBuilder.add_system()` and `SimulationBuilder.add_resource()`. To add
  these, users need to encapsulate their content within a plugin
- Flake8 configuration from `setup.cfg`

### Fixed

- Bug in Business operating hours regex that did not recognize AM/PM strings
- `setup.cfg` did not properly include data files in the wheel build.