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

# Install dependencies (in Ubuntu/Debian—on RedHat-based platforms, use yum instead).
# This will automatically start rabbitmq-server when the server starts.
sudo apt-get install rabbitmq-server build-essential autoconf libtool pkg-config python-dev libxml2-dev libxslt1-dev zlib1g-dev

# Within the webroot directory, install the Python dependencies.
sudo pip install -r requirements.txt

# Install gunicorn, which is the Django WSGI web server we'll be running that Nginx or Apache will proxy to.
sudo pip install gunicorn

# Set up your site's config file. The default site config is in opendata/, and an example settings file is
# at settings_example.py. Rename it to settings.py and edit the config options to suit your purposes. You
# must sign up for and provide a Bing API key.
cd opendata
mv settings_example.py settings.py
pico settings.py

# just run this and then follow the prompts as appropriate to set up the DB.
# this will also set up the superuser you use to log into the /admin
python manage.py syncdb

# Start Django w/ Gunicorn. Make sure to specify the PID file, so you can stop it again later.
gunicorn -D -p gunicorn.pid --access-logfile access.log --error-logfile error.log opendata.wsgi

# Launch Celery, which will manage the search API requests. Use screen to run this `screen` to keep it
# running in the background, and reattach to Celery to stop it with Ctrl-C.
celery -A opendata worker -l info

# Now it's installed and running!

# If you need to stop the currently running Gunicorn instance:
kill `cat gunicorn.pid`
```

## Colophon

This tool was made by [SVSG](http://svsg.co/) for [U.S. Open Data](https://usopendata.org/).
