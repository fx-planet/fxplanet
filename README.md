# fxplanet / Ligthworks FX


## System requirements

* Linux compatible environment
* Python 3.4+ (3.6 recommended)
* PostgreSQL database server (9.x+)


## Installation


```
make initialize-postgres
make
make migrate
```

In case of troubles with virtualenv please try to create environment
manually:

```
virtualenv -p python3 env
```

and run `make` again.


## Settings


All local settings can be placed in `fxplanet/settings_local.py`.

Settings defined in this file will *override* base settings
(`fxplanet/settings.py`).


## Running dev server

```
make runserver
```

or

```
./manage runserver
```

Open browser with http://127.0.0.1:8000/


To change a port call:

```
make runserver PORT=8001
```

or

```
./manage runserver 8001
```


## Management commands

Use `manage` to call Django's management commands. This is a wrapper
which automatically activates Python's virtual environment.

Examples:

1. Run Django shell

```
./manage shell
```

2. Execute migrations

```
./manage migrate
```

## Docker quick-start

* Ensure media files are in fxplanet/media
* Ensure database dump is in top level directory as fxplanet.sql.gz
* docker-compose up

## Helpful links

* https://docs.djangoproject.com/en/2.0/
* https://wiki.postgresql.org/wiki/Client_Authentication
* https://www.postgresql.org/docs/9.1/static/auth-methods.html
