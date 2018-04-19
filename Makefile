.PHONY: development requirements.txt requirements-dev.txt manage
PORT=8000


development : env-activate init requirements.txt requirements-dev.txt


production : env-activate init requirements.txt


fxplanet/settings_local.py :
	touch fxplanet/settings_local.py


init : fxplanet/settings_local.py
	@mkdir -p fxplanet/templates
	@mkdir -p fxplanet/static
	@mkdir -p fxplanet/static_collected
	@mkdir -p fxplanet/media
	@mkdir -p var/log
	@mkdir -p var/tmp
	@mkdir -p var/run


requirements.txt :
	(source env/bin/activate && pip install -r $@)


requirements-dev.txt :
	(source env/bin/activate && pip install -r $@)


env:
	(virtualenv -p python3 env)


env-activate: env
	(source env/bin/activate)


runserver:
	(source env/bin/activate && python manage.py runserver $(PORT))


migrate:
	(source env/bin/activate && python manage.py migrate)


shell:
	(source env/bin/activate && python manage.py shell)


makemigrations:
	(source env/bin/activate && python manage.py makemigrations)


initialize-postgres:
	createdb fxplanet
