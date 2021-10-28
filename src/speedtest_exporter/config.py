import yaml
import logging
import os

class configmanager:
    def __init__(self):
        #Set default config, so the app works regardless if any are provided
        self.app_port = 8000
        self.polling_interval = 300

    def open_file(self,file_path):
        #check if config file provided exists and open it.
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                logging.info('Config file has been opened sucessfully')
                try: 
                    yaml.scan(f)
                    return yaml.safe_load(f)
                except yaml.scanner.ScannerError:
                    #Fail app if config file can not be read properly following yaml standards.
                    logging.critical('Unable to tokenize the config file. Please check config file format.')
                    raise
                
        else:
            #Raise a FileNotFoundError if file does not exist
            raise FileNotFoundError
            

    def parse_config(self):
        #Open file and update the config values
        try:
            config = self.open_file('config.yml')
        except FileNotFoundError:
            logging.warning('Config file not found. Default config will be loaded.')
        else:
            self.app_port,self.polling_interval = config['port'],config['poll_interval']
            logging.info('Config parsed and loaded, the exporter will run on port %s with a polling interval of %s' %(self.app_port,self.polling_interval))
