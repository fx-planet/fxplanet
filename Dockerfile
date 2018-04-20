FROM python:3.4-jessie

# Dependencies. All for Pillow
RUN apt-get update && apt-get install -y xvfb \
    git wget python-numpy python-scipy netpbm \
    python-qt4 ghostscript libffi-dev libjpeg-turbo-progs \
    python-setuptools python-virtualenv \
    python-dev python3-dev cmake \
    libtiff5-dev zlib1g-dev \
    libcairo2-dev libjpeg62-turbo-dev libpango1.0-dev libgif-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev \
    python-tk python3-tk \
    libharfbuzz-dev libfribidi-dev && apt-get clean

# Make bash our shell
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Add files required to bootstrap
ADD catalog              /app/catalog
ADD fxplanet             /app/fxplanet
ADD Makefile             /app
ADD manage               /app
ADD manage.py            /app
ADD requirements.txt     /app
ADD requirements-dev.txt /app

# Bootstrap. Needs setuptools installed in the virtualenv
WORKDIR /app
RUN virtualenv -p python3 env
RUN source env/bin/activate && pip install -U setuptools
RUN make

RUN mkdir -p /app/fxplanet/static_collected

EXPOSE 8000

# Run each time when the container starts
CMD source env/bin/activate && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
