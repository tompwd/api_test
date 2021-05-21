# Foobar

This API allows querying of the policy database, including these tables / views:
- calendar
- finance
- policy
- policy_lifecycle

It also provides the code to produce the policy_lifecycle view

## Installation

Open project and activate the virtual environment

```bash
. .venv/bin/activate
```

## Usage

#### Creation of the sqlite.db (OPTIONAL)

#### Creation of Policy Lifecycle Table (OPTIONAL)

#### Running Unit Tests

#### Using the API

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```
