import json
from configuration import db

class Movie(db.Model):
    # This class allows for the creation and storage of movie objects in a database.
    # Each field represents a property of the movie, and its data type is specified.
    __tablename__ = 'movies'
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    director = db.Column(db.String(80), unique=False, nullable=False)
    genre = db.Column(db.Text, nullable=False)  # Stores genres in a JSON serialized format.
    release_year = db.Column(db.Integer, unique=False, nullable=False)
    duration = db.Column(db.Integer, unique=False, nullable=False)
    favourite = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    is_animated = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    watched = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    age_rating = db.Column(db.Integer, unique=False, nullable=False)
    
    def to_json(self):
        """Converts the movie object into a JSON-compatible dictionary."""
        return {
            "movieId": self.movie_id,
            "title": self.title,
            "genre": self.get_genres(),  # Retrieve the genres as a list.
            "releaseYear": self.release_year,
            "favourite": self.favourite,
            "duration": self.duration,
            "isAnimated": self.is_animated,
            "watched": self.watched,
            "ageRating": self.age_rating
        }

    def set_genres(self, genres):
        """Sets the genres for the movie by serializing a unique list of genres into a JSON string."""
        if not all(isinstance(genre, str) for genre in genres):
            raise ValueError("All genres must be strings")
        unique_genres = list(set(genres))  # Remove duplicates from the genres list.
        self.genre = json.dumps(unique_genres)

    def get_genres(self):
        """Gets the genres of the movie by deserializing the JSON string into a list."""
        return json.loads(self.genre)

    def add_genre(self, new_genre):
        """Adds a new genre to the movie while ensuring no duplicates exist."""
        genres = set(self.get_genres())  # Convert existing genres to a set for uniqueness.
        genres.add(new_genre)  # Add the new genre to the set.
        self.set_genres(list(genres))  # Update the genre field with the new list.

    def __repr__(self):
        """Provides a string representation of the movie object for debugging purposes."""
        return f"<Movie {self.title} ({self.release_year})>"


