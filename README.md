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

to change a port:

```
make runserver PORT=8001
```


## Helpful links

* https://docs.djangoproject.com/en/2.0/
* https://wiki.postgresql.org/wiki/Client_Authentication
* https://www.postgresql.org/docs/9.1/static/auth-methods.html
