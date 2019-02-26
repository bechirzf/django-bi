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

1. Add "bi" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'bi',
    ]

2. Add OBJECTS_PATH setting like this::

    OBJECTS_PATH='objects',

3. Include the bi URLconf in your project urls.py like this::

    path('', include('bi.urls')),

4. Run `python manage.py migrate` to create the bi models.

5. Start the development server.

6. Visit http://127.0.0.1:8000/ to see your dashboards.
