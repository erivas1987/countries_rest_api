import configparser
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from models import Country, db

#Initialize the configParser
configParser = configparser.RawConfigParser()   
configFilePath = r'app_config.ini'
configParser.read(configFilePath)

#Configuring the logging
logging.basicConfig(filename=configParser.get('Logging','log_file'),
                level=logging.getLevelName(configParser.get('Logging','log_level')), format=configParser.get('Logging','log_format'))

def configScheduler(job,job_args,frequency):
    """
    Creates and configures the scheduler object. 
    The scheduler object could be used to execute a background task while the app is running 
    job: The function to call every time the job triggers
    job_args: The arguments to the job function
    frequency: The interval in minutes that the job will execute the function.
    Return: None
    """
    scheduler = BackgroundScheduler()
    #TODO: get job parameters from app_config.ini file to avoid hardcoded values
    job = scheduler.add_job(job, 'interval',args=job_args, minutes=frequency)
    logging.getLogger('apscheduler').setLevel(logging.ERROR)
    scheduler.start()