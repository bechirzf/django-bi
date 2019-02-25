=====
Business intelligence
=====

BI is a simple Django app to conduct business intelligence.

Quick start
-----------

1. Add "reporting" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'reporting',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('', include('reporting.urls')),

3. Run `python manage.py migrate` to create the bi models.

4. Start the development server.

5. Visit http://127.0.0.1:8000/ to see your dashboards.
