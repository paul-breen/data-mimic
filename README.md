## Data Mimic

This project enables dynamic visualisations of overlaid schematics.  In particular, it can use a PLC Data Server (PDS) as its data source, thereby providing SCADA-like mimics.

This project consists of the datamimic modules, and a simple Flask web application, to provide a web API to access the mimics.

### Running the application

Create a `.env` file, in the parent directory of the application file (`App.py`).  This `.env` file should contain the path to the Flask app, and the path to the mimics configuration file (`mimics.json`).  Then from that directory, run:

```bash
flask run
```

For example, to run the dummy-data example, create a `.env` file that looks like:

```bash
FLASK_APP=datamimic/App.py
MIMICS_CONF=datamimic/examples/dummy-data/mimics.json

```

then start the application:

```bash
flask run
```

and point a browser at http://127.0.0.1:5000/mimic/update/engine to access the API, or http://127.0.0.1:5000/mimic/view/engine to access the simple web application views.  The top-level view http://127.0.0.1:5000/ will list links to all available mimics.

This example uses calls to `random.randint()` as its data source, and generates random values to drive the mimic.

To run the application under a standalone WSGI server, such as `gunicorn`, do:

```bash
gunicorn -b <host>:<port> datamimic.App:app
```

using the same `.env` file as above.

### Custom web application

To create a custom web application, say, based on a PDS, requires an application configuration (`mimics.json`), background images for the mimics, and optionally custom template files to override the defaults.  Given a directory structure like:

```bash
app-dir
|
+-.env
|
+-config
| |
| +-images
| | |
| | +-background-1.png
| |
| +-mimics.json
|
+-templates
  |
  +-list-views.html
  +-view.html
```

the configuration will need to specify paths to the images and templates thus:

```json
{
    "global": {
        "design_mode": false,
        "template_folder": "/path/to/app-dir/templates"
    },
    "mimics": [
        {
            "module": "datamimic.PdsBaseMimic",
            "class": "PdsBaseMimic",
            "id": "mimic_1",
            "figsize": [12,6],
            "bg_image": "/path/to/app-dir/config/images/background-1.png",
            "objects": [
                {
...
 
```

and a `.env` file something like:

```bash
FLASK_APP=/usr/lib/python3.6/site-packages/datamimic/App.py
MIMICS_CONF=/path/to/app-dir/config/mimics.json
```

with the correct installation path for the `datamimic` package.

