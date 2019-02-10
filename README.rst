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

- Patch config file (PATH_TO_CONFIG_DEFAULT) with API keys, this will create config file copy - PATH_TO_CONFIG_FILE

    .. code-block::
    
        export PATH_TO_CONFIG_FILE = {YOUR_PATH_TO_CONFIG_FILE}
        export FACE_PLUS_PLUS_API_KEY = {YOUR_FACE_PLUS_PLUS_API_KEY}
        export FLICKR_API_KEY = {YOUR_FLICKR_API_KEY}
        
        python patch_config.py --config {PATH_TO_CONFIG_DEFAULT}

- Pure python

    .. code-block::

        python int_20h_test/main.py --config {PATH_TO_CONFIG_FILE}

- With gunicorn

    .. code-block::

        gunicorn --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker "int20h_test.main:create_app('{PATH_TO_CONFIG_FILE}')"


API:
----

- GET /get_photos

    - Emotions ids:

        - SADNESS_ID=0
        - NEUTRAL_ID=1
        - DISGUST_ID=2
        - ANGER_ID=3
        - SURPRISE_ID=4
        - FEAR_ID=5
        - HAPPINESS_ID=6

    - Request:

        .. code-block::

            {
                emotions: [array<int>] - Arrays of emotions ids,
                from_id: [int] - This photo with tis id will be not included in result,
                count: [int] - Count of photos to return
            }

    - Response:

        .. code-block::

            {
                status: [string(OK|ERR)] - response status,
                photos_urls: [array<{
                    id: [int] - Photo id,
                    url: [string] - Photo url
                }>] - Photos info sorted by id
            }



Deployment
-------------------

Application is running on heroku service and can be found here - https://int20h-test.herokuapp.com/
