from configuration import db, app
from models import Movie  
#This file was created for testing purposes to clear the database
with app.app_context():
    # Clear all records from the Movie table
    db.session.query(Movie).delete()
    db.session.commit()
    print("All records cleared from the database.")
