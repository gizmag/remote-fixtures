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
