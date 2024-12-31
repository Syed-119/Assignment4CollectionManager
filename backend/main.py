from flask import request, jsonify
from configuration import app, db
from models import Movie, Documentary
import json


#This endpoint searches the data base and returns the movies. I will be adding filtering to this
@app.route("/search_movies", methods=["GET"])
def search_movies():
    # Get query parameters
    title = request.args.get("title")
    director = request.args.get("director")
    genre = request.args.get("genre")
    age_rating = request.args.get("ageRating")
    favourite = request.args.get("favourite")
    watched = request.args.get("watched")
    releaseYear = request.args.get("releaseYear")
    duration = request.args.get("duration")
    type = request.args.get("type")

    # Build the query dynamically based on the filters provided
    query = Movie.query

    if title is not None:
        query = query.filter(Movie.title.ilike(f"%{title}%"))  # Case-insensitive partial match
    if director is not None:
        query = query.filter(Movie.director.ilike(f"{director}"))
    if genre is not None:
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))  # Case-insensitive partial match
    if age_rating is not None:
        query = query.filter(Movie.age_rating == int(age_rating))
    if favourite is not None:
        query = query.filter(Movie.favourite == (favourite.lower() == "true"))
    if watched is not None:
        query = query.filter(Movie.watched == (watched.lower() == "true"))
    if releaseYear is not None:
        query = query.filter(Movie.release_year >= releaseYear )
    if duration is not None:
        query = query.filter(Movie.duration<= duration )
    if type is not None:
        query = query.filter(Movie.type.ilike(f"{type}"))

    # Execute the query and convert results to JSON
    movies = query.all()
    json_movies = [movie.to_json() for movie in movies]

    return jsonify({"movies": json_movies}), 200


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
    movie_type = data.get("type")  # New field to specify if it's a documentary or regular movie
    topic = data.get("topic")  # Documentary-specific field
    documentarian = data.get("documentarian")  # Documentary-specific field

    # Validate required fields
    if not title or not director or not release_year or not duration or not age_rating or not genre:
        return jsonify({"message": "You must include title, director, release year, duration, age rating, and genre"}), 400
    
    genre_json = json.dumps(genre)  # Serialize genre as JSON string

    if movie_type == "documentary":
        # Create a documentary object
        if not topic or not documentarian:
            return jsonify({"message": "Documentary must include topic and documentarian"}), 400

        # Create the documentary object, using the base 'Movie' fields along with documentary-specific fields
        new_movie = Documentary(
            title=title, 
            director=director, 
            genre=genre_json,  # Store genre as a JSON string
            release_year=release_year, 
            duration=duration, 
            favourite=favourite, 
            is_animated=is_animated, 
            watched=watched, 
            age_rating=age_rating, 
            topic=topic,
            documentarian=documentarian,
            type=movie_type
        )

    elif movie_type == "movie":
        # Create a regular movie object
        new_movie = Movie(
            title=title, 
            director=director, 
            genre=genre_json,  # Store genre as a JSON string
            release_year=release_year, 
            duration=duration, 
            favourite=favourite, 
            is_animated=is_animated, 
            watched=watched, 
            age_rating=age_rating,
            type=movie_type
        )
    
    # Add the movie/documentary to the database and commit
    try:
        db.session.add(new_movie)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Movie/Documentary Added"}), 201



#This endpoint updates a movie record depedning on the fields in the request data
#The movie id is passed in to specify the individual record to be updated
#The movie record can be marked as 'Watched' or can be favourited.
@app.route("/update_movie/<int:movie_id>", methods=["PATCH"])
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({"message": "Movie not found"}), 404
    
    data = request.json
    # Update only the fields provided in the request
    if "watched" in data:
        movie.watched = data.get("watched", movie.watched)
    if "favourite" in data:
        movie.favourite = data.get("favourite", movie.favourite)

    db.session.commit()

    return jsonify({"message": "Movie updated successfully"}), 200

#This endpoint will delete a movie based on the title, director and genre passed in the request.
#It uses SQL Alchemy ORM to perform a delete query on the data base
@app.route("/delete_movie", methods=["POST"])
def delete_movie():
    title = request.json.get("title")
    director = request.json.get("director")
    genre = request.json.get("genre")
    
    if not title or not director or not genre:
        return jsonify({"message": "You must include the title, director, and genre"}), 400

    # Use ORM to delete
    movie = Movie.query.filter_by(title=title, director=director, genre=genre).first()

    if movie:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({"message": "Movie deleted successfully"}), 200
    else:
        return jsonify({"message": "Movie not found"}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
