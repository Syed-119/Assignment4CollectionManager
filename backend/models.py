import json
from configuration import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Movie(db.Model):
    # This class allows for the creation and storage of movie objects in a database.
    # Each field represents a property of the movie, and its data type is specified.
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    director = db.Column(db.String(80), unique=False, nullable=False)
    genre = db.Column(db.Text, nullable=False)  # Stores genres in a JSON serialized format.
    release_year = db.Column(db.Integer, unique=False, nullable=False)
    duration = db.Column(db.Integer, unique=False, nullable=False)
    favourite = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    is_animated = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    watched = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    age_rating = db.Column(db.Integer, unique=False, nullable=False)
    type = db.Column(db.String(50))  # Discriminator column to distinguish subclasses.

    __mapper_args__ = {
        'polymorphic_identity': 'movie',  # Identifier for the base class.
        'polymorphic_on': type  # Specifies the column used to differentiate subclasses.
    }

    def to_json(self):
        """Converts the movie object into a JSON-compatible dictionary."""
        return {
            "movieId": self.movie_id,
            "title": self.title,
            "director": self.director,
            "genre": self.get_genres(),  # Retrieve the genres as a list.
            "releaseYear": self.release_year,
            "favourite": self.favourite,
            "duration": self.duration,
            "isAnimated": self.is_animated,
            "watched": self.watched,
            "ageRating": self.age_rating,
            "type":self.type
        }
        
    def set_genres(self, genres):
        """Sets the genres for the movie by serializing a unique list of genres into a JSON string."""
        if not all(isinstance(genre, str) for genre in genres):
            raise ValueError("All genres must be strings")
        unique_genres = list(set(genres))  # Remove duplicates from the genres list.
        self.genre = json.dumps(unique_genres)

    def get_genres(self):
        if not self.genre:  # Handle None or empty string
            return []
        try:
            return json.loads(self.genre)
        except json.JSONDecodeError:
            return []  # Handle invalid JSON

    def add_genre(self, new_genre):
        """Adds a new genre to the movie while ensuring no duplicates exist."""
        genres = set(self.get_genres())  # Convert existing genres to a set for uniqueness.
        genres.add(new_genre)  # Add the new genre to the set.
        self.set_genres(list(genres))  # Update the genre field with the new list.

    def __repr__(self):
        """Provides a string representation of the movie object for debugging purposes."""
        return f"<Movie {self.title} ({self.release_year})>"


class Documentary(Movie):
    # This class represents documentaries and inherits properties from the Movie class.
    # Additional attributes specific to documentaries are defined here.
    __tablename__ = 'documentaries'

    documentary_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), primary_key=True)
    topic = db.Column(db.String(128), nullable=False)  # Topic of the documentary.
    documentarian = db.Column(db.String(80), nullable=False)  # Name of the person who made the documentary.

    __mapper_args__ = {
        'polymorphic_identity': 'documentary',  # Identifier for the Documentary subclass.

    }
    
    def to_json(self):
        """Converts the documentary object into a JSON-compatible dictionary, 
        extending the base movie attributes with documentary-specific fields."""
        movie_json = super().to_json()  # Start with the base class JSON representation.
        movie_json.update({
            "documentaryId": self.documentary_id,
            "topic": self.topic,
            "documentarian": self.documentarian,
            "type":self.type
        })
        return movie_json

    def __repr__(self):
        """Provides a string representation of the documentary object for debugging purposes."""
        return f"<Documentary {self.title} ({self.release_year})>"

class KidMovies(Movie):
    __tablename__ = "kidMovies"

    kid_movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), primary_key=True)
    moral_lesson = db.Column(db.String(512), nullable=False)
    parental_appeal = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'kidMovie'  # Identifier for the Kids Movie subclass.
    }

    def to_json(self):
        movie_json = super().to_json()
        movie_json.update({
            "kidMovieId": self.kid_movie_id,
            "moralLesson": self.moral_lesson,
            "parentalAppeal":self.parental_appeal,
            "type":self.type 
        })
        return movie_json
    
    def __repr__(self):
        """Provides a string representation of the kids movie object for debugging purposes."""
        return f"<Kid Movie {self.title} ({self.release_year})>"

        

