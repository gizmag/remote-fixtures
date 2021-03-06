Django Remote Fixtures
===============

[![Build Status](https://travis-ci.org/gizmag/remote-fixtures.png?branch=master)](https://travis-ci.org/gizmag/remote-fixtures)
[![Coverage Status](https://coveralls.io/repos/gizmag/remote-fixtures/badge.png?branch=master)](https://coveralls.io/r/gizmag/remote-fixtures?branch=master)

This library lets you dump out your current database into the dumpdata .json
format and upload it to S3 automatically. You're then able to load the data back
in on the other end.

Python 2.7 with Django 1.5+ is supported. If you would like to add support for
your environment feel free to
[fork the repository](https://github.com/gizmag/remote-fixtures/fork).

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
REMOTE_FIXTURES_BUCKET = 'myproject_fixtures'
```

Note that the `REMOTE_FIXTURES_BUCKET` will need to be manually created through
the AWS control panel.

### Cache

Optionally, you can cache generated fixture files on your machine to greatly
speed up subsequent pulls. The fixture files will however take up disk space.

To configure the cache add to your settings

```python
REMOTE_FIXTURES_ENABLE_CACHE = True  # default is False
REMOTE_FIXTURES_BASE_CACHE_PATH = '/my/path/'  # defaults to ~/.remote_fixture_cache
```

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
fixture_2013-12-02t064449268866.json   17.4MB    02 Dec 2013  1 month ago
fixture_2013-12-03t045828313027.json   23.6MB    03 Dec 2013  4 weeks, 1 day ago
fixture_2013-12-03t064841764321.json   23.6MB    03 Dec 2013  4 weeks, 1 day ago
fixture_2013-12-10t054540615336.json   23.9MB    10 Dec 2013  3 weeks, 1 day ago
fixture_2013-12-11t022818593030.json   27.1MB    11 Dec 2013  3 weeks, 1 day ago
fixture_2013-12-13t052205908111.json   24.1MB    13 Dec 2013  2 weeks, 5 days ago
fixture_2013-12-16t100033009137.json   108.6MB   16 Dec 2013  2 weeks, 2 days ago
fixture_2013-12-23t042152487261.json   129.5KB   23 Dec 2013  1 week, 3 days ago
fixture_2013-11-30t042815968252.json   129.7KB   23 Dec 2013  1 week, 3 days ago
```

### Compression

By default your fixture files will be gzip compressed by `push_fixtures` and
transparently decompressed by `pull_fixtures`. In my tests I've found a 4-10x
file size reduction with compression enabled. If you do not wish for your
fixture files to be compressed, pass the `--nocompress` option to
`push_fixtures`.
