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

and point a browser at http://127.0.0.1:5000/mimic/update/engine.

This example uses calls to `random.randint()` as its data source, and generates random values to drive the mimic.

