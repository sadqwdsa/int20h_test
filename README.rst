===================
Test app for INT20H
===================

Get started
----------------

1. Create a Python virtual environment.

    .. code-block::

        python3 -m virtualenv venv

2. Activate virtualenv.

    .. code-block::

        source venv/bin/activate

3. Install requirements

    .. code-block::

        pip install -r requirements.txt


How to run:
-----------

- Pure python

    .. code-block::

        python int_20h_test/main.py --config {PATH_TO_CONFIG_FILE}

- With gunicorn

    .. code-block::

        gunicorn --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker "int20h_test.main:create_app('{PATH_TO_CONFIG_FILE}')"


API:
----

- GET /get_photos

    - Request:

        .. code-block::

            {
                emotions: Arrays of emotions ids
            }

    - Response:

        .. code-block::

            {
                status: OK|ERR,
                photos_urls: Array of photos urls
            }


Deployment
-------------------

::TODO
