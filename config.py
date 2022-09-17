import configparser
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from models import Country, db

#Initialize the configParser
config_parser = configparser.RawConfigParser()   
config_file_path = r'app_config.ini'
config_parser.read(config_file_path)

#Configuring the logging
logging.basicConfig(filename=config_parser.get('Logging','log_file'),
                level=logging.getLevelName(config_parser.get('Logging','log_level')), format=config_parser.get('Logging','log_format'))

def config_scheduler(job,job_args,frequency):
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