.. image:: https://img.shields.io/travis/zhelyabuzhsky/django-bi.svg
    :target: https://travis-ci.org/zhelyabuzhsky/django-bi
.. image:: https://img.shields.io/pypi/v/django-bi.svg
    :target: https://pypi.org/project/django-bi/
.. image:: https://img.shields.io/pypi/dm/django-bi.svg
    :target: https://pypi.org/project/django-bi/

=====================
Business intelligence
=====================

BI is a simple Django app to conduct business intelligence.

Quick start
-----------

1. Add "reporting" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'reporting',
    ]

2. Include the bi URLconf in your project urls.py like this::

    path('', include('reporting.urls')),

3. Run `python manage.py migrate` to create the bi models.

4. Start the development server.

5. Visit http://127.0.0.1:8000/ to see your dashboards.
