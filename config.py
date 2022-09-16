import configparser

#Initialize the configParser
configParser = configparser.RawConfigParser()   
configFilePath = r'app_config.ini'
configParser.read(configFilePath)
