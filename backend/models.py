import json
from configuration import db

class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    director = db.Column(db.String(80), unique=False, nullable=False)
    genre = db.Column(db.Text, nullable=False)
    release_year = db.Column(db.Integer, unique=False, nullable=False)
    duration = db.Column(db.Integer, unique=False, nullable=False)
    favourite = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    is_animated = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    watched = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    age_rating = db.Column(db.Integer, unique=False, nullable=False)

    def to_json(self):
        return {
            "movieId": self.movie_id,
            "title": self.title,
            "genre": self.get_genres(),  
            "releaseYear": self.release_year,
            "favourite": self.favourite,
            "duration": self.duration,
            "isAnimated": self.is_animated,
            "watched": self.watched,
            "ageRating": self.age_rating
        }

    def set_genres(self, genres):
        """Serialize a unique list of genres (like a set) into a JSON string."""
        if not all(isinstance(genre, str) for genre in genres):
            raise ValueError("All genres must be strings")
        unique_genres = list(set(genres))  
        self.genre = json.dumps(unique_genres)

    def get_genres(self):
        """Deserialize the JSON string back into a list."""
        return json.loads(self.genre)

    def add_genre(self, new_genre):
        """Add a single genre, ensuring no duplicates."""
        genres = set(self.get_genres())  
        genres.add(new_genre)  
        self.set_genres(list(genres)) 

    def toggle_favourite(self):
        self.favourite = not self.favourite

    def toggle_watched(self):
        self.watched = not self.watched

    def __repr__(self):
        return f"<Movie {self.title} ({self.release_year})>"
