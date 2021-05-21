# <ins>API Test for Cuvva<ins>

This API allows querying of the policy database, including these tables / views:
- calendar
- finance
- policy
- policy_lifecycle

It also provides the code to produce the policy_lifecycle view

## Assumptions



## Installation

Open project and activate the virtual environment

```bash
. .venv/bin/activate
```

## Usage

### <ins>Creation of the sqlite.db (OPTIONAL)<ins>

I have provided a completed sqlite.db file in the project, but if you would like to recreate this from scratch, you can
do this by running the db_setup.py files found in the src folder.

Or by running this command in the terminal:

```bash
python3 src.db_setup.py
```

### <ins>Creation of Policy Lifecycle Table (OPTIONAL)<ins>

The provided aqlite.db file already has this view added, but if you are recreating this file, you will also need to
recreate this view. This can be done by running the policy_lifecycle_view.py file in the src folder.

Or by running this command in the terminal

```bash
python3 src.policy_lifecycle_view.py
```

### <ins>Running Unit Tests<ins>

The unit tests should be automatically found in your IDE using pytest as the testing provider. You may need to set
pytest as the testing provider in your IDE setting if it is not already configured.

Steps to follow for testing:

1. start up the web service API by running the api.py file or using the following command:
```bash
python3 api.py
```

2. You can now run all tests or individual tests from your IDE testing functionality

### <ins>Using the API<ins>

Once the API service is running you can access the various services using the URL's specified in the code. I have
provided below a few example URL's to try to see the outputs.

- Total policy count for a given user
    - http://127.0.0.1:5000/api/v1/resources/user/policy/count?user_id=%27user_000000BzeQ5BO4Urilu5LCOwr09eT%27
- Total days active for a given user
    - http://127.0.0.1:5000/api/v1/resources/user/days_active/count?user_id=%27user_000000C4wvsbftmmdew81vUDGDwjx%27
- Total new user count for a given date
    - http://127.0.0.1:5000/api/v1/resources/policy/new/count?date=%272020-03-04%27
- Total lapsed user count for a given month
    - http://127.0.0.1:5000/api/v1/resources/policy/lapsed/count?month=%272021-02%27&underwriter=%27red%27
- Total new users premium per date for a given underwriter
    - http://127.0.0.1:5000/api/v1/resources/policy/new/premium?underwriter=%27red%27&month=%272020-03%27
- Pull all policy data
    - http://127.0.0.1:5000/api/v1/resources/policy?underwriter=%27red%27

## Contributions
- Tom Stowers - 21/05/2021
