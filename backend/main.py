from flask import request, jsonify
from configuration import app, db
from models import Movie, Documentary
import json

#This endpoint searches the data base and returns the movies. I will be adding filtering to this
@app.route("/search_movies", methods=["GET"])
def search_movies():
    movies = Movie.query.all()
    json_movies = list(map(lambda x: x.to_json(), movies))
    return jsonify({"movies": json_movies})

#This endpoint is responsible for adding movies or documentaries to the database
#The fields are retrieved from the request data and are mapped, depending on the type of record, so that they can be stored in the database
@app.route("/add_movies", methods=["POST"])
def add_movie():
    data = request.json
    movie_type = data.get("type")

    if not movie_type:
        return jsonify({"error": "Missing 'type' field to specify movie type"}), 400

    try:
        if movie_type == "movie":
            new_movie = Movie(
                title=data["title"],
                director=data["director"],
                genre=json.dumps(data["genre"]) if isinstance(data["genre"], list) else data["genre"],
                release_year=data["releaseYear"],
                duration=data["duration"],
                favourite=data.get("favourite", False),
                is_animated=data["isAnimated"],
                watched=data["watched"],
                age_rating=data["ageRating"]
            )
            db.session.add(new_movie)

        elif movie_type == "documentary":
            new_documentary = Documentary(
                title=data["title"],
                director=data["director"],
                genre=json.dumps(data["genre"]) if isinstance(data["genre"], list) else data["genre"],
                release_year=data["releaseYear"],
                duration=data["duration"],
                favourite=data.get("favourite", False),
                is_animated=data["isAnimated"],
                watched=data["watched"],
                age_rating=data["ageRating"],
                topic=data["topic"],
                documentarian=data["documentarian"]
            )
            db.session.add(new_documentary)

        else:
            return jsonify({"error": f"Unsupported movie type: {movie_type}"}), 400

        db.session.commit()
        return jsonify({"message": f"{movie_type.capitalize()} added successfully"}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
