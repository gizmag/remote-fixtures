Django Remote Fixtures
===============

This library lets you dump out your current database into the dumpdata .json
format and upload it to S3 automatically. You're then able to load the data back
in on the other end.

## Setup

First, install this library with pip

```bash
pip install git+https://github.com/gizmag/remote-fixtures.git#egg=remote-fixtures
```

Then, add the app to INSTALLED_APPS in your settings file

```python
INSTALLED_APPS = (
    ...
    'remote_fixtures',
)
```

And add in your AWS details

```python
AWS_ACCESS_KEY = '...'
AWS_SECRET_ACCESS_KEY = '...'
REMOTE_FIXTURE_BUCKET = 'myproject_fixtures'
```

Note that the `REMOTE_FIXTURE_BUCKET` will need to be manually created through
the AWS control panel.

## Usage

### `push_fixtures`

This command is used to upload your fixtures to S3, it is used like

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
