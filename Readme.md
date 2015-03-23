# Let Me Get That Data For You (LMGTDFY)

LMGTDFY is a web-based utility to catalog all open data file formats found on a given domain name. It finds CSV, XML, JSON, XLS, XLSX, XML, and Shapefiles, and makes the resulting inventory available for download as a CSV file. It does this using Bing’s API.

This is intended for people who need to inventory all data files on a given domain name—these are generally employees of state and municipal government, who are creating an open data repository, and performing the initial step of figuring out what data is already being emitted by their government.

LMGTDFY powers [U.S. Open Data’s LMGTDFY site](http://lmgtdfy.usopendata.org/), but anybody can install the software and use it to create their own inventory. You might want to do this if you have more than 2,000 data files on your site. U.S. Open Data’s LMGTDFY site caps the number of results at 2,000, in order to avoid winding up with an untenably large invoice for using Bing’s API. ([Microsoft allows 5,000 searches/month for free](https://datamarket.azure.com/dataset/bing/search), but has kindly provided U.S. Open Data with a substantial sponsorship for this service, in the form of API credits.)

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

You will probably want to edit `TIME_ZONE` and `SEARCH_PER_QUERY` (the maximum number of results to get from Bing, per site), and you have to provie your Bing API key as `BING_KEY`. If you’re deploying a live site, you’ll want to set `DEBUG` to `False`.

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

This will manage the search API requests. Use screen to run this `screen` to keep it running in the background, and reattach to Celery to stop it with Ctrl-C. The `--autoscale` option specifies how many (and how few) copies of Celery you want running at one time—basically, how many people who think are going to be trying to request data on your site at once. `10,2` means that it allows a maximum of 10, and always has at least 2 instances running.

```
celery -A opendata worker -l info --autoscale=10,2
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

You'll probably want to set up Gunicorn and Celery to run continuously, and to start and stop along with your server. Here are [instructions on daemonizing Gunicorn](https://gunicorn-docs.readthedocs.org/en/latest/deploy.html) and [instructions on daemonizing Celery](https://celery.readthedocs.org/en/latest/tutorials/daemonizing.html).

## Colophon

This tool was made by [Ted Han](https://github.com/knowtheory) and [SVSG](http://svsg.co/) for [U.S. Open Data](https://usopendata.org/).
