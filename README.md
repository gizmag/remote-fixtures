Django Remote Fixtures
===============

This library lets you dump out your current database into the dumpdata .json
format and upload it to S3 automatically. You're then able to load the data back
in on the other end.

## Setup

First, install this library with `pip`

```bash
pip install remote-fixtures
```

Then, add the app to `INSTALLED_APPS` in your settings file

```python
INSTALLED_APPS += (
    'remote_fixtures',
)
```

And add in your AWS details

```python
AWS_ACCESS_KEY_ID = '...'
AWS_SECRET_ACCESS_KEY = '...'
REMOTE_FIXTURE_BUCKET = 'myproject_fixtures'
```

Note that the `REMOTE_FIXTURE_BUCKET` will need to be manually created through
the AWS control panel.

## Usage

### `push_fixtures`

This command is used to upload your fixtures to S3.

```bash
# upload all fixtures
python manage.py push_fixtures

# upload fixtures for a single app
python manage.py push_fixtures users

# upload fixtures for a single model
python manage.py push_fixtures articles.Article

# combine them together
python manage.py push_fixtures articles.Article users
```

It will output the filename that was generated for the file. This can be used to
specify an exact fixture file to install.

### `pull_fixtures`

This command is used to pull fixtures from S3, and load them. By default it
will load the last set of fixtures uploaded. You can also optionally specify a
specific filename to be loaded.

Only files that begin with `fixture_` will be considered to be loaded.

```bash
# download / load last set of fixtures
python manage.py pull_fixtures

# download a specific fixture file
python manage.py pull_fixtures fixture_2013-11-30t050929030986.json
```

### `list_fixtures`

To list off fixtures in your S3 bucket, simply run
`python manage.py list_fixtures`.

```bash
python manage.py list_fixtures
fixture_2013-12-02t064449268866.json     17.4MB     02 Dec 2013     1 month ago
fixture_2013-12-03t045828313027.json     23.6MB     03 Dec 2013     4 weeks, 1 day ago
fixture_2013-12-03t064841764321.json     23.6MB     03 Dec 2013     4 weeks, 1 day ago
fixture_2013-12-10t054540615336.json     23.9MB     10 Dec 2013     3 weeks, 1 day ago
fixture_2013-12-11t022818593030.json     27.1MB     11 Dec 2013     3 weeks, 1 day ago
fixture_2013-12-13t052205908111.json     24.1MB     13 Dec 2013     2 weeks, 5 days ago
fixture_2013-12-16t100033009137.json     108.6MB    16 Dec 2013     2 weeks, 2 days ago
fixture_2013-12-23t042152487261.json     129.5KB    23 Dec 2013     1 week, 2 days ago
```
