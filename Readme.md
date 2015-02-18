# Let Me Get That Data For You (LMGTDFY)

Good day sir/madam, do you make data accessible on your website?  You might, and may not even know it.  Thankfully, we here at LMGTDFY can help you with that exact problem.

Our python, django and celery driven website can help identify data located on your website quickly and easily for the low introductory price of absolutely free and open source.

## Is it any good?

Yes.

## Sounds too good to be true! What's the catch?

If you wish to run your own copy of the site, you will need to sign up for Microsoft's Azure marketplace in order to get an access key for Bing's search API.

## Installation

### Download and install the contents of this repository

### Install OS dependencies

In Ubuntu/Debian—on RedHat-based platforms, use yum instead. This will automatically start the RabbitMQ messaging service when the server starts.

```
sudo apt-get install rabbitmq-server build-essential autoconf libtool pkg-config python-dev libxml2-dev libxslt1-dev zlib1g-dev
```

### Install Python dependencies

Within the webroot directory (e.g., `/var/www/example.com/`), install the Python dependencies.

```
sudo pip install -r requirements.txt
```

### Install Gunicorn

That’s the Django WSGI web server we'll be running, which Nginx or Apache will proxy to.

```
sudo pip install gunicorn
```

### Configure LMGTDFY

Set up your site's config file. The default site config is in [`opendata/`](https://github.com/opendata/lmgtdfy/tree/master/opendata), and an example settings file is at [`settings_example.py`](https://github.com/opendata/lmgtdfy/blob/master/opendata/settings_example.py). Rename it to `settings.py` and edit the config options to suit your purposes. At a minimum, you must sign up for and provide a Bing API key.

```
cd opendata
mv settings_example.py settings.py
pico settings.py
```

### Set up the application

Follow the prompts as appropriate to set up the database. This will also set up the superuser you use to log into the site’s `/admin` page.

```
python manage.py syncdb
```

### Start Django with Gunicorn

Make sure to specify the PID file, so you can stop it again later.

````
gunicorn -D -p gunicorn.pid --access-logfile access.log --error-logfile error.log opendata.wsgi
```

### Launch Celery

This will manage the search API requests. Use screen to run this `screen` to keep it running in the background, and reattach to Celery to stop it with Ctrl-C.

```
celery -A opendata worker -l info
```

### Proxy it through Apache/Nginx

Pass all requests through to Gunicorn, except for any requests to `static/`. For instance, in Apache, you'd set up something like this:

```
ProxyPass /static !
ProxyPass / http://localhost:8000/
ProxyPassReverse / http://localhost:8000/
```

### Final configuration

By default, no domains are whitelisted—you have to specify which TLDs or domains that you want to permit people to get data for. That's because Bing API queries cost money, so you might want to restrict it. Log in to `http://example.com/admin` (using your site’s domain name) and add any TLDs (e.g., `gov`) or domain names that you want to allow site visitors to index.

### Also

Note that if you need to stop the currently running Gunicorn instance, you can run:

```
kill `cat gunicorn.pid`
```

### Finally

You'll probably want to set up Gunicorn and Celery to run continuously, and to start and stop along with your server. Here are [instructions on daemonizing Gunicorn](http://gunicorn-docs.readthedocs.org/en/latest/deploy.html) and [instructions on daemonizing Celery](http://celery.readthedocs.org/en/latest/tutorials/daemonizing.html).

## Colophon

This tool was made by [Ted Han](/knowtheory) and [SVSG](http://svsg.co/) for [U.S. Open Data](https://usopendata.org/).
