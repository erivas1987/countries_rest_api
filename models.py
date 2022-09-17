
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Create db model for Country
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    capital = db.Column(db.String(256), nullable=False)
    area = db.Column(db.Integer)

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id'      : self.id,
           'name'    : self.name,
           'capital' : self.capital,
           'area'    : self.area
       }

    #Defining the way an instance of Country object will be printed
    def __repr__(self):
        return "{0} with {1} mk2".format(self.name, self.area)


def initialize_db_data(logger):
    """sumary_line
    Adds some initial Countries data in the database.
    This function runs only one time, when the database is created. 
    Keyword arguments:
    logger -- A logger object for 
    Return: None
    """
    logger.info("Adding test data to database")
    thailand = Country(name="Thailand", capital = "Bangkok", area = 513120)
    australia = Country(name="Australia", capital = "Canberra", area = 7617930)
    egypt = Country(name="Egypt", capital = "Cairo", area = 1010408)
    cuba = Country(name="Cuba", capital ="Habana", area = 110860)
    for country in (thailand, australia, egypt, cuba):
        db.session.add(country) 
    db.session.commit()
    logger.info("Test data added successfully to the database")
