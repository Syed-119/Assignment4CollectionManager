from flask import request, jsonify
from configuration import app, db
from models import Movie

@app.route("/movies", methods=["GET"])
def get_movies():
    movies = Movie.query.all()
    json_movies = list(map(lambda x: x.to_json(), movies))
    return jsonify({"movies": json_movies})

@app.route("/add_movies", methods=["POST"])
def add_movie():
    title = request.json.get("title")
    director = request.json.get("director")
    genre = request.json.get("genre")
    release_year = request.json.get("releaseYear")
    duration = request.json.get("duration")
    favourite = request.json.get("favourite")
    is_animated = request.json.get("isAnimated")
    watched = request.json.get("watched")
    age_rating = request.json.get("ageRating")

    if not title or not release_year or not duration or not watched or not age_rating or not genre or not is_animated:
        return (jsonify({"message":"You must include title, release year, duration, watched, age rating, genre, and animated"})
                , 400
                )
    
    new_movie = Movie(title=title, director=director, genre=genre, release_year=release_year, duration=duration, favourite=favourite, is_animated=is_animated, watched=watched, age_rating=age_rating)

    try:
        db.session.add(new_movie)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Movie Added"}), 201

@app.route("/update_movie/<int:movie_id>", methods=["PATCH"])
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({"message": "Movie not found"}), 404
    
    data = request.json
    movie.watched = data.get("watched", movie.watched)

    db.session.commit()

    return jsonify({"message": "User updated"}), 200

@app.route("/delete_movie", methods=["POST"])
def delete_movie():
    title = request.json.get("title")
    director = request.json.get("director")
    genre = request.json.get("genre")
    
    if not title or not director or not genre:
        return jsonify({"message": "You must include the title, director and genre"})
    
    try: 
        db.session.execute("DELETE FROM movie WHERE title = :title AND director = :director AND genre = :genre", 
                        {"title": title, "director": director, "genre": genre})
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Movie Deleted Successfully"}), 201



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
