from flask import request, jsonify
from configuration import app, db
from models import Movie, Documentary, KidMovies
import json


#This endpoint searches the data base and returns the movies. I will be adding filtering to this
@app.route("/search_movies", methods=["GET"])
def search_movies():
    # Get query parameters
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

    # Start building the query
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
            return jsonify({"message": "Invalid age rating format"}), 400
    
    # Execute the query and convert results to JSON
    movies = query.all()
    json_movies = [movie.to_json() for movie in movies]

    return jsonify({"movies": json_movies})


#This endpoint is responsible for adding movies or documentaries to the database
#The fields are retrieved from the request data and are mapped, depending on the type of record, so that they can be stored in the database
@app.route("/add_movies", methods=["POST"])
def add_movie():
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
    movie_type = data.get("type")  # New field to specify the type
    topic = data.get("topic")  # Documentary-specific field
    documentarian = data.get("documentarian")  # Documentary-specific field
    moral_lesson = data.get("moralLesson")
    parental_appeal = data.get("parentalAppeal")

    # Validate required fields
    if not title or not director or not release_year or not duration or not age_rating or not genre:
        return jsonify({"message": "Missing required fields"}), 400

    # Create the appropriate subclass instance based on `type`
    new_movie = None
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
    try:
        new_movie.set_genres(genre)  # Use set_genres to handle genres
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    # Save to database
    try:
        db.session.add(new_movie)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Movie/Documentary Added"}), 201



#This endpoint updates a movie record depedning on the fields in the request data
#The movie id is passed in to specify the individual record to be updated
@app.route("/update_movie/<int:movie_id>", methods=["PATCH"])
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({"message": "Movie not found"}), 404
    
    # Check if it's a KidMovie instance
    if isinstance(movie, KidMovies):
        # Handle KidMovies-specific updates
        data = request.json
        if "moralLesson" in data:
            movie.moral_lesson = data["moralLesson"]
        if "parentalAppeal" in data:
            movie.parental_appeal = data["parentalAppeal"]
    elif isinstance(movie, Documentary):
        data = request.json
        if "topic" in data:
            movie.topic = data["topic"]
        if "documentarian" in data:
            movie.documentarian = data["documentarian"]
    
    # Handle other movie fields (common to all movies)
    data = request.json
    if "title" in data:
        movie.title = data.get("title", movie.title)
    if "director" in data:
        movie.director = data.get("director", movie.director)
    if "genre" in data:
        movie.set_genres(data.get("genre", movie.get_genres()))  # Use set_genres for genre update
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



#This endpoint will delete a movie based on the title, director and genre passed in the request.
#It uses SQL Alchemy ORM to perform a delete query on the data base
@app.route("/delete_movie/<int:id>", methods=["DELETE"])
def delete_movie(id):
    movie = Movie.query.get(id)
    
    if not movie:
        return jsonify({"message": "Movie not found"}), 404
    
    db.session.delete(movie)
    db.session.commit()
    
    return jsonify({"message": "Movie deleted"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

