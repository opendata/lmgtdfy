# Let Me Get That Data For You (LMGTDFY)

Good day sir/madam, do you make data accessible on your website?  You might, and may not even know it.  Thankfully, we here at LMGTDFY can help you with that exact problem.

Our python, django and celery driven website can help identify data located on your website quickly and easily for the low introductory price of absolutely free and open source.

## Is it any good?

Yes.

## Sounds too good to be true! What's the catch?

If you wish to run your own copy of the site, you will need to sign up for Microsoft's Azure marketplace in order to get an access key for Bing's search API.

## Installation

```
## download and install the contents of this repository

# install dependencies in ubuntu/debian
# this will automatically start rabbitmq-server when the machine starts, so you won't need to fiddle with it.
sudo apt-get install rabbitmq-server build-essential autoconf libtool pkg-config python-dev libxml2-dev libxslt1-dev zlib1g-dev

# install python dependencies
pip install -r -requirements

# install gunicorn, which is the django WSGI web server we'll be running that nginx (or apache) will proxy to.
pip install gunicorn

# just run this and then follow the prompts as appropriate to set up the DB.
# this will also set up the superuser you use to log into the /admin
python manage.py syncdb

# start django w/ gunicorn.  make sure to specify the pid file so you can stop it again later
gunicorn -D -p gunicorn.pid --access-logfile access.log --error-logfile error.log opendata.wsgi

# stop the currently running unicorn (in the event you need to restart things)
kill `cat gunicorn.pid`

# use screen to run this `screen` to keep it running in the background
# you'll just use ctrl+c to stop celery
celery -A opendata worker -l info
```

## Colophon

This tool was made by [SVSG](http://svsg.co/) for [U.S. Open Data](https://usopendata.org/).
