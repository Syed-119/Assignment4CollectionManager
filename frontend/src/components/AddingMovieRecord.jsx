import React, { useState } from "react";
import MovieList from "./MovieList";

const AddingMovieRecord = ({ action, existingMovie = {}, updateCallBack, params, setParams }) => {
    // State variables to hold form data
    const [title, setTitle] = useState(existingMovie.title || "");
    const [director, setDirector] = useState(existingMovie.director || "");
    const [genre, setGenre] = useState(existingMovie.genre || "");
    const [releaseYear, setReleaseYear] = useState(existingMovie.releaseYear || "");
    const [duration, setDuration] = useState(existingMovie.duration || "");
    const [watched, setWatched] = useState(existingMovie.watched || false);
    const [favourite, setFavourite] = useState(existingMovie.favourite || false);
    const [isAnimated, setIsAnimated] = useState(existingMovie.isAnimated || false);
    const [ageRating, setAgeRating] = useState(existingMovie.ageRating || "");
    const [movieType, setMovieType] = useState(existingMovie.movieType || "");  // Default type is "movie"
    const [topic, setTopic] = useState(existingMovie.topic || "");  // Specific to documentaries
    const [documentarian, setDocumentarian] = useState(existingMovie.documentarian || "");  // Specific to documentaries
    const [moralLesson, setMoralLesson] = useState(existingMovie.moralLesson || "");
    const [parentalAppeal, setParentalAppeal] = useState(existingMovie.parentalAppeal || "");



    const updating = Object.entries(existingMovie).length !== 0

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Prepare the request to backend depending on if its a search or adding action
        if (action === "add") {


            const movieRecord = {
                title,
                director,
                genre: (typeof genre === "string" ? genre : String(genre || "")).split(",").map((g) => g.trim()), // Split and clean up the genres
                releaseYear: parseInt(releaseYear, 10),
                duration: parseInt(duration, 10),
                favourite,
                isAnimated,
                watched,
                ageRating,
                type: movieType,
                topic,  // Only used for documentaries
                documentarian,  // Only used for documentaries
                moralLesson, // Only used for kids movies
                parentalAppeal // Only used for kids movies
            };

            // Send the movie record to the backend
            const url = "http://127.0.0.1:5000/" + (updating ? `update_movie/${existingMovie.movieId}` : "add_movies");
            const options = {
                method: updating ? "PATCH" : "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(movieRecord),
            };

            console.log("Request URL:", url);
            console.log("Request Options:", options);

            const response = await fetch(url, options);

            // Handle the response based on status
            if (response.status !== 201 && response.status !== 200) {
                const data = await response.json();
                alert(data.message);  // Show any error message from the server
            } else {
                updateCallBack()
                alert("Movied added/updated successfully")
            }
        } else if (action === "search") {
            const parameters = new URLSearchParams();

            if (title) parameters.append("title", title);
            if (director) parameters.append("director", director);
            if (genre) parameters.append("genre", genre);
            if (ageRating) parameters.append("age_rating", ageRating);
            if (favourite) parameters.append("favourite", favourite);
            if (watched) parameters.append("watched", watched);
            if (releaseYear) parameters.append("release_year", releaseYear);
            if (movieType) parameters.append("type", movieType);
            if (topic) parameters.append("topic", topic);
            if (documentarian) parameters.append("documentarian", documentarian);

            setParams(parameters)
        }
    };


    return (
        <div>
            <form onSubmit={handleSubmit}>
                {/* Movie Type Selection */}
                <div>
                    <label htmlFor="movieType">Movie Type:</label>
                    <select
                        id="movieType"
                        value={movieType}
                        onChange={(e) => setMovieType(e.target.value)}
                    >
                        <option value="movie">Regular Movie</option>
                        <option value="documentary">Documentary</option>
                        <option value="kidMovie">Kids Movie</option>
                    </select>
                </div>



                {/* Movie Title */}
                <div>
                    <label htmlFor="title">Movie Title:</label>
                    <input
                        type="text"
                        id="title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required={action === "add"}
                    />
                </div>

                {/* Director */}
                <div>
                    <label htmlFor="director">Director:</label>
                    <input
                        type="text"
                        id="director"
                        value={director}
                        onChange={(e) => setDirector(e.target.value)}
                        required={action === "add"}
                    />
                </div>

                {/* Genre - Accepts a comma-separated list of genres */}
                <div>
                    <label htmlFor="genre">Genre:</label>
                    <input
                        type="text"
                        id="genre"
                        value={genre}
                        onChange={(e) => setGenre(e.target.value)}
                        required={action === "add"}
                    />
                </div>

                {/* Release Year */}
                <div>
                    <label htmlFor="releaseYear">Release Year:</label>
                    <input
                        type="number"
                        id="releaseYear"
                        value={releaseYear}
                        onChange={(e) => setReleaseYear(e.target.value)}
                        required={action === "add"}
                    />
                </div>

                {/* Duration in minutes */}
                <div>
                    <label htmlFor="duration">Duration (in minutes):</label>
                    <input
                        type="number"
                        id="duration"
                        value={duration}
                        onChange={(e) => setDuration(e.target.value)}
                        required={action === "add"}
                    />
                </div>

                {/* Watched checkbox */}
                <div>
                    <label htmlFor="watched">Watched:</label>
                    <input
                        type="checkbox"
                        id="watched"
                        checked={watched}
                        onChange={() => setWatched(!watched)}  // Toggle the watched state

                    />
                </div>

                {/* Favourite checkbox */}
                <div>
                    <label htmlFor="favourite">Favourite:</label>
                    <input
                        type="checkbox"
                        id="favourite"
                        checked={favourite}
                        onChange={() => setFavourite(!favourite)}  // Toggle the favourite state

                    />
                </div>

                {/* Is Animated checkbox */}
                <div>
                    <label htmlFor="isAnimated">Is Animated:</label>
                    <input
                        type="checkbox"
                        id="isAnimated"
                        checked={isAnimated}
                        onChange={() => setIsAnimated(!isAnimated)}  // Toggle the isAnimated state

                    />
                </div>

                {/* Age Rating */}
                <div>
                    <label htmlFor="ageRating">Age Rating:</label>
                    <input
                        type="text"
                        id="ageRating"
                        value={ageRating}
                        onChange={(e) => setAgeRating(e.target.value)}
                        required={action === "add"}
                    />
                </div>

                {/* Display these fields only if movie type is documentary */}
                {movieType === "documentary" && (
                    <>
                        <div>
                            <label htmlFor="topic">Topic:</label>
                            <input
                                type="text"
                                id="topic"
                                value={topic}
                                onChange={(e) => setTopic(e.target.value)}
                                required={action === "add"}
                            />
                        </div>
                        <div>
                            <label htmlFor="documentarian">Documentarian:</label>
                            <input
                                type="text"
                                id="documentarian"
                                value={documentarian}
                                onChange={(e) => setDocumentarian(e.target.value)}
                                required={action === "add"}

                            />
                        </div>
                    </>
                )}

                {movieType === "kidMovie" && (
                    <>
                        <div>
                            <label htmlFor="moralLesson">Moral Lesson:</label>
                            <input
                                type="text"
                                id="moralLesson"
                                value={moralLesson}
                                onChange={(e) => setMoralLesson(e.target.value)}
                                required={action === "add"}
                            />
                        </div>
                        <div>
                            <label htmlFor="parentalAppeal">Parental Appeal:</label>
                            <input
                                type="number"
                                id="parentalAppeal"
                                value={parentalAppeal}
                                min="1"
                                max="10"
                                onChange={(e) => {
                                    const value = parseInt(e.target.value, 10);
                                    if (value >= 1 && value <= 10) {
                                        setParentalAppeal(value); // Update state only if value is within range
                                    } else if (e.target.value === "") {
                                        setParentalAppeal(""); // Allow clearing the input
                                    }
                                }}
                                required={action === "add"}
                            />
                        </div>
                    </>
                )}

                <button type="submit">{updating ? "Update" : action === "add" ? "Add Movie" : "Search Movie"}</button>


            </form>
        </div>
    );
};

export default AddingMovieRecord;
