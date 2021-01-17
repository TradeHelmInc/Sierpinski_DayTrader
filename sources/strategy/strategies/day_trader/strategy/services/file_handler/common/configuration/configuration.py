import configparser

class Configuration:
    def __init__(self, configFile):
        config = configparser.ConfigParser()
        config.read(configFile)

        self.InputPath = config['DEFAULT']['INPUT_PATH']
        self.OutputPath = config['DEFAULT']['OUTPUT_PATH']
        self.FailedPath = config['DEFAULT']['FAILED_PATH']
        self.ProcessedPath = config['DEFAULT']['PROCESSED_PATH']

        self.Mode = config['DEFAULT']['MODE']
