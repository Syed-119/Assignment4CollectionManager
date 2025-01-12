from flask import request, jsonify
from configuration import app, db
from models import Movie, Documentary, KidMovies
import json

# Endpoint to search movies in the database with optional filters
@app.route("/search_movies", methods=["GET"])
def search_movies():
    # Extract query parameters for filtering
    title = request.args.get("title")
    director = request.args.get("director")
    genre = request.args.get("genre")
    age_rating = request.args.get("age_rating")
    favourite = request.args.get("favourite")
    watched = request.args.get("watched")
    release_year = request.args.get("release_year")
    duration = request.args.get("duration")
    movie_type = request.args.get("type")
    is_animated = request.args.get("is_animated")
    topic = request.args.get("topic")
    documentarian = request.args.get("documentarian")
    moral_lesson = request.args.get("moral_lesson")
    parental_appeal = request.args.get("parental_appeal")

    # Build the SQLAlchemy query based on provided filters
    query = Movie.query
    if title:
        query = query.filter(Movie.title.ilike(f"%{title}%"))
    if topic:
        query = query.filter(Movie.topic.ilike(f"%{topic}%"))
    if documentarian:
        query = query.filter(Movie.documentarian.ilike(f"%{documentarian}%"))
    if moral_lesson:
        query = query.filter(Movie.moral_lesson.ilike(f"%{moral_lesson}%"))
    if director:
        query = query.filter(Movie.director.ilike(f"%{director}%"))
    if genre:
        query = query.filter(Movie.genre.contains(f'"{genre}"'))
    if age_rating:
        try:
            query = query.filter(Movie.age_rating == int(age_rating))
        except ValueError:
            return jsonify({"message": "Invalid age rating format"}), 400
    if favourite is not None:
        query = query.filter(Movie.favourite == (favourite.lower() == "true"))
    if watched is not None:
        query = query.filter(Movie.watched == (watched.lower() == "true"))
    if release_year:
        try:
            query = query.filter(Movie.release_year <= int(release_year))
        except ValueError:
            return jsonify({"message": "Invalid release year format"}), 400
    if duration:
        try:
            query = query.filter(Movie.duration <= int(duration))
        except ValueError:
            return jsonify({"message": "Invalid duration format"}), 400
    if movie_type and movie_type.lower() != "all":
        query = query.filter(Movie.type.ilike(f"{movie_type}"))
    if is_animated is not None:
        query = query.filter(Movie.is_animated == (is_animated.lower() == "true"))
    if parental_appeal:
        try:
            query = query.filter(Movie.parental_appeal <= int(parental_appeal))
        except ValueError:
            return jsonify({"message": "Invalid parental appeal format"}), 400
    
    # Execute the query and return results
    movies = query.all()
    json_movies = [movie.to_json() for movie in movies]
    return jsonify({"movies": json_movies})


# Endpoint to add new movies or documentaries to the database
@app.route("/add_movies", methods=["POST"])
def add_movie():
    # Parse input data from request
    data = request.json
    title = data.get("title")
    director = data.get("director")
    genre = data.get("genre")
    release_year = data.get("releaseYear")
    duration = data.get("duration")
    favourite = data.get("favourite")
    is_animated = data.get("isAnimated")
    watched = data.get("watched")
    age_rating = data.get("ageRating")
    movie_type = data.get("type")
    topic = data.get("topic")
    documentarian = data.get("documentarian")
    moral_lesson = data.get("moralLesson")
    parental_appeal = data.get("parentalAppeal")

    # Validate required fields for all movie types
    if not title or not director or not release_year or not duration or not age_rating or not genre:
        return jsonify({"message": "Missing required fields"}), 400

    # Determine movie type and create the appropriate database record
    if movie_type == "documentary":
        if not topic or not documentarian:
            return jsonify({"message": "Documentary must include topic and documentarian"}), 400
        new_movie = Documentary(
            title=title,
            director=director,
            release_year=release_year,
            duration=duration,
            favourite=favourite,
            is_animated=is_animated,
            watched=watched,
            age_rating=age_rating,
            topic=topic,
            documentarian=documentarian
        )
    elif movie_type == "kidMovie":
        if not moral_lesson or not parental_appeal:
            return jsonify({"message": "Kids Movie must include moral lesson and parental appeal"}), 400
        new_movie = KidMovies(
            title=title,
            director=director,
            release_year=release_year,
            duration=duration,
            favourite=favourite,
            is_animated=is_animated,
            watched=watched,
            age_rating=age_rating,
            moral_lesson=moral_lesson,
            parental_appeal=parental_appeal
        )
    elif movie_type == "movie":
        new_movie = Movie(
            title=title,
            director=director,
            release_year=release_year,
            duration=duration,
            favourite=favourite,
            is_animated=is_animated,
            watched=watched,
            age_rating=age_rating
        )
    else:
        return jsonify({"message": "Invalid movie type"}), 400

    # Set genres and save the movie to the database
    try:
        new_movie.set_genres(genre)
        db.session.add(new_movie)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Movie/Documentary Added"}), 201


# Endpoint to update an existing movie record by ID
@app.route("/update_movie/<int:movie_id>", methods=["PATCH"])
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({"message": "Movie not found"}), 404

    # Handle updates specific to KidMovies
    if isinstance(movie, KidMovies):
        data = request.json
        if "moralLesson" in data:
            movie.moral_lesson = data["moralLesson"]
        if "parentalAppeal" in data:
            movie.parental_appeal = data["parentalAppeal"]

    # Handle updates specific to Documentaries
    elif isinstance(movie, Documentary):
        data = request.json
        if "topic" in data:
            movie.topic = data["topic"]
        if "documentarian" in data:
            movie.documentarian = data["documentarian"]

    # Handle updates for common movie fields
    data = request.json
    if "title" in data:
        movie.title = data.get("title", movie.title)
    if "director" in data:
        movie.director = data.get("director", movie.director)
    if "genre" in data:
        movie.set_genres(data.get("genre", movie.get_genres()))
    if "releaseYear" in data:
        movie.release_year = data.get("releaseYear", movie.release_year)
    if "duration" in data:
        movie.duration = data.get("duration", movie.duration)
    if "isAnimated" in data:
        movie.is_animated = data.get("isAnimated", movie.is_animated)
    if "ageRating" in data:
        movie.age_rating = data.get("ageRating", movie.age_rating)
    if "watched" in data:
        movie.watched = data.get("watched", movie.watched)
    if "favourite" in data:
        movie.favourite = data.get("favourite", movie.favourite)

    db.session.commit()
    return jsonify({"message": "Movie updated successfully"}), 200


# Endpoint to delete a movie by ID
@app.route("/delete_movie/<int:id>", methods=["DELETE"])
def delete_movie(id):
    movie = Movie.query.get(id)
    
    if not movie:
        return jsonify({"message": "Movie not found"}), 404
    
    # Remove the movie from the database
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie deleted"}), 200


if __name__ == '__main__':
    # Initialize the database and start the server
    with app.app_context():
        db.create_all()

    app.run(debug=True)
