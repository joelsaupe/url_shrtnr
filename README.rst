=====
URL Shrtnr
=====

URL Shrtnr is a basic URL Shortener app. It allows a user to enter a
web address and receive a shortened version that may be used to view
the original website.

Quick start
-----------

1. Add "url_shrntr" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'url_shrtnr',
    )

2. Include the url_shrtnr URLconf in your project urls.py at the very end. This is so that the other urls will take priority over
the slugs.::
	...
    url(r'^shrtnr/', include('url_shrtnr.urls')),
    url(r'^(?P<slug>.+)/', url_shrtnr.views.UrlLoader.as_view()),

3. Run `python manage.py migrate` to create the models.

4. Change the domain to localhost:8000 (or whatever you are using), in both the views.py and shrtnr.js files.

5. Start the development server and visit http://127.0.0.1:8000/shrtnr/ to create a shortened url.

5. Copy the link and paste it into the browser.