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
    # Assuming the genre column stores genres as JSON strings and you want to search for the genre in the list
        query = query.filter(Movie.genre.contains(f'"{genre}"'))  # Use contains for partial match in the JSON string
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
    json_movies = list(map(lambda x: x.to_json(), movies))
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
    movie_type = data.get("type")  # New field to specify if it's a documentary or regular movie
    topic = data.get("topic")  # Documentary-specific field
    documentarian = data.get("documentarian")  # Documentary-specific field
    moral_lesson = data.get("moralLesson")
    parental_appeal = data.get("parentalAppeal")

    # Validate required fields
    if not title or not director or not release_year or not duration or not age_rating or not genre:
        return jsonify({"message": "You must include title, director, release year, duration, age rating, and genre"}), 400
    
    
    
    if movie_type == "documentary" or movie_type== "kidMovie":
        if movie_type == "documentary":
            if not topic or not documentarian:
                return jsonify({"message": "Documentary must include topic and documentarian"}), 400
        elif movie_type == "kidMovie":
            if not moral_lesson or not parental_appeal:
                    return jsonify({"message": "Kids Movie must include a moral lesson and a parental appeal rating"}), 400
            
        new_movie = Movie(
            title=title, 
            director=director, 
            release_year=release_year, 
            duration=duration, 
            favourite=favourite, 
            is_animated=is_animated, 
            watched=watched, 
            age_rating=age_rating,
            type=movie_type
        )
    
    elif movie_type == "movie":
        # Create a regular movie object
        new_movie = Movie(
            title=title, 
            director=director,
            release_year=release_year, 
            duration=duration, 
            favourite=favourite, 
            is_animated=is_animated, 
            watched=watched, 
            age_rating=age_rating,
            type=movie_type
        )
    new_movie.set_genres(genre) #Using custom method to add genres
        
    # Add the movie/documentary to the database and commit
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

