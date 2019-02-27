FROM alpine

# Based on https://github.com/hellt/nginx-uwsgi-flask-alpine-docker/tree/master/python3
MAINTAINER niels@dutchsec.com

COPY requirements.txt /tmp/requirements.txt

RUN apk add --no-cache \
python3 \
bash \
nginx \
uwsgi \
uwsgi-python3 \
supervisor && \
python3 -m ensurepip && \
rm -r /usr/lib/python*/ensurepip && \
pip3 install --upgrade pip setuptools && \
pip3 install -r /tmp/requirements.txt && \
rm /etc/nginx/conf.d/default.conf && \
rm -r /root/.cache

# Config files
COPY nginx.conf /etc/nginx/
COPY flask-site-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/supervisord.conf

# Prepare static dir
COPY ./static/ /static

# Python server scripts
COPY server.py /server.py
COPY channels.py /channels.py
COPY utils.py /utils.py

CMD ["/usr/bin/supervisord"]
