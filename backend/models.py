import json
from configuration import db
from sqlalchemy.orm import Mapped, mapped_column

class Base(db.Model):
    """Base class for all database models. Provides common functionality and is not tied to a specific table."""
    __abstract__ = True  # Indicates this is an abstract class and should not have a corresponding table.

    def to_json(self):
        """Converts the object into a JSON-compatible dictionary."""
        raise NotImplementedError("Subclasses must implement the `to_json` method.")

    def __repr__(self):
        """Provides a string representation of the object for debugging purposes."""
        raise NotImplementedError("Subclasses must implement the `__repr__` method.")

class Movie(Base):
    """
    Represents a general movie.
    Defines shared fields and functionality for all movie-related models, 
    such as title, director, and release year.
    """
    __tablename__ = 'movies'
    
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    director = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.Text, nullable=False)  # Stores genres in a serialized JSON format.
    release_year = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    favourite = db.Column(db.Boolean, default=False)
    is_animated = db.Column(db.Boolean, default=False)
    watched = db.Column(db.Boolean, default=False)
    age_rating = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50))  # Discriminator column to distinguish subclasses.

    __mapper_args__ = {
        'polymorphic_identity': 'movie',  # Identifier for the Movie class.
        'polymorphic_on': type  # Column used to differentiate between subclasses.
    }

    def to_json(self):
        """Converts the movie object into a dictionary format compatible with JSON."""
        return {
            "movieId": self.movie_id,
            "title": self.title,
            "director": self.director,
            "genre": self.get_genres(),
            "releaseYear": self.release_year,
            "favourite": self.favourite,
            "duration": self.duration,
            "isAnimated": self.is_animated,
            "watched": self.watched,
            "ageRating": self.age_rating,
            "type": self.type
        }
        
    def set_genres(self, genres):
        """Sets the genres for the movie as a unique JSON-serialized list."""
        if not all(isinstance(genre, str) for genre in genres):
            raise ValueError("All genres must be strings")
        unique_genres = list(set(genres))
        self.genre = json.dumps(unique_genres)

    def get_genres(self):
        """Retrieves genres as a list, handling cases of missing or invalid data."""
        if not self.genre:  # Handle None or empty string
            return []
        try:
            return json.loads(self.genre)  # Deserialize JSON to list
        except json.JSONDecodeError:
            return []  # Handle invalid JSON

    def __repr__(self):
        """Provides a human-readable string representation of the movie."""
        return f"<Movie {self.title} ({self.release_year})>"

class Documentary(Movie):
    """
    Represents a documentary, inheriting shared fields from the Movie class 
    and adding specific fields such as topic and documentarian.
    """
    __tablename__ = 'documentaries'
    
    documentary_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), primary_key=True)
    topic = db.Column(db.String(128), nullable=False)
    documentarian = db.Column(db.String(80), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'documentary'  # Identifier for the Documentary subclass.
    }

    def to_json(self):
        """Extends the base JSON representation with fields specific to documentaries."""
        movie_json = super().to_json()
        movie_json.update({
            "documentaryId": self.documentary_id,
            "topic": self.topic,
            "documentarian": self.documentarian,
            "type": self.type
        })
        return movie_json

    def __repr__(self):
        """Provides a human-readable string representation of the documentary."""
        return f"<Documentary {self.title} ({self.release_year})>"

class KidMovies(Movie):
    """
    Represents kids' movies, inheriting shared fields from the Movie class 
    and adding specific fields such as moral lesson and parental appeal.
    """
    __tablename__ = "kidMovies"

    kid_movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), primary_key=True)
    moral_lesson = db.Column(db.String(512), nullable=False)  # Description of the moral lesson (string).
    parental_appeal = db.Column(db.Integer, nullable=False)  # Parental appeal score (integer).

    __mapper_args__ = {
        'polymorphic_identity': 'kidMovie'  # Identifier for the Kids Movie subclass.
    }

    def to_json(self):
        """Extends the base JSON representation with fields specific to kids' movies."""
        movie_json = super().to_json()
       
