from prometheus_client import Gauge, start_http_server
import speedtest
import time
import config
import logging

logging.basicConfig(
    level = logging.INFO, 
    format = '{asctime} {levelname:<4} {message}', 
    style = '{',
    datefmt='%d/%m/%Y %H:%M')

def speedtester():
    speedtester = speedtest.Speedtest()
    speedtester.download(),speedtester.upload()

    return speedtester.results.dict()

class SpeedtestExporter:
    def __init__(self, polling_interval_seconds):
        self.polling_interval = polling_interval_seconds

        #Metrics to collect:
        self.ping_latency = Gauge('ping_latency', 'The time takes for a small data set to be transmitted')
        self.download_bandwith = Gauge('download_bandwith', 'How much data can be downloaded in a second in bytes')
        self.upload_bandwith = Gauge('upload_bandwith', 'How much data can be uploaded in a second in bytes')

    def metrics_loop(self):
        #Run a loop that collects the data data and then sleeps for X amount of time to control the interval.
        while True:
            self.fetch()
            time.sleep(self.polling_interval)

    def fetch(self):
        try:
            metrics = speedtester()

            #Update metrics with currenct values
            self.ping_latency.set(metrics['ping'])
            self.download_bandwith.set(metrics['download'])
            self.upload_bandwith.set(metrics['upload'])

        except (IndexError, speedtest.SpeedtestBestServerFailure):
            #Take care of the IndexError for now. 
            print("Something else went wrong")
            


def main():
    #Load config
    configuration_loader = config.configmanager()
    configuration_loader.parse_config()

    exporter = SpeedtestExporter(polling_interval_seconds=configuration_loader.polling_interval)
    
    #Start the prom client server under the desired port. 
    start_http_server(configuration_loader.app_port)
    exporter.metrics_loop()



if __name__ == "__main__":
    main()
