# Speedtest Exporter for Prometheus in Python

A simple server that scrapes [Speedtest](https://www.speedtest.net) and exports them via HTTP for [Prometheus](https://prometheus.io/)
consumption.


Run locally
===========

1. Install dependencies:
```bash
pip3 install -r requirement.txt
```

2. Run the app
```bash
python3 ./src/speedtest_exporter/exporter.py
```

Run in a Docker containter
==========================

1. Build the docker image
```
docker build -tag speedtest_exporter .
```

2.  Run the docker image
```
docker run -d -p 8000:8000 speedtest_exporter
```

Configuration
=============

By default the app will run on port 8000 and scrape metrics every 5 minutes. You can change that by editing the config.yml file. If you change the port make sure to change the docker port when running the container. 


Metrics
=======

+ ping_latency
+ download_bandwith
+ upload_bandwith
