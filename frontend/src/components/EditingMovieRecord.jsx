import React, { useState } from "react";
import MovieList from "./MovieList";

const EditingMovieRecord = ({ action, existingMovie = {}, updateCallBack, params, setParams }) => {
    // State variables to hold form data for movie fields
    const [title, setTitle] = useState(existingMovie.title || "");
    const [director, setDirector] = useState(existingMovie.director || "");
    const [genre, setGenre] = useState(existingMovie.genre || "");
    const [releaseYear, setReleaseYear] = useState(existingMovie.releaseYear || "");
    const [duration, setDuration] = useState(existingMovie.duration || "");
    const [watched, setWatched] = useState(existingMovie.watched || "");
    const [favourite, setFavourite] = useState(existingMovie.favourite || "");
    const [isAnimated, setIsAnimated] = useState(existingMovie.isAnimated || "");
    const [ageRating, setAgeRating] = useState(existingMovie.ageRating || "");
    const [movieType, setMovieType] = useState(existingMovie.type || "movie");  // Default type is "movie"
    const [topic, setTopic] = useState(existingMovie.topic || "");  // Specific to documentaries
    const [documentarian, setDocumentarian] = useState(existingMovie.documentarian || "");  // Specific to documentaries
    const [moralLesson, setMoralLesson] = useState(existingMovie.moralLesson || ""); // Specific to kids' movies
    const [parentalAppeal, setParentalAppeal] = useState(existingMovie.parentalAppeal || ""); // Specific to kids' movies

    // Determine if the form is for updating an existing movie
    const updating = Object.entries(existingMovie).length !== 0;

    // Handle form submission based on the action (add or search)
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Adding or updating a movie
        if (action === "add") {
            const movieRecord = {
                title,
                director,
                genre: (typeof genre === "string" ? genre : String(genre || "")).split(",").map((g) => g.trim()), // Split and clean up the genres
                releaseYear: parseInt(releaseYear, 10),
                duration: parseInt(duration, 10),
                favourite: favourite === "true" || favourite === true,
                isAnimated: isAnimated === "true" || isAnimated === true,
                watched: watched === "true" || watched === true,
                ageRating,
                type: movieType,
                topic, // Only used for documentaries
                documentarian, // Only used for documentaries
                moralLesson, // Only used for kids movies
                parentalAppeal, // Only used for kids movies
            };

            // Send the movie record to the backend (add or update)
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
                console.log("movies:", data);
                alert(data.message); // Show any error message from the server
            } else {
                alert("Movie added/updated successfully");
                updateCallBack(); // Refresh the movie list after adding/updating
            }
        }
        // Searching for movies based on the input criteria
        else if (action === "search") {
            const parameters = new URLSearchParams();

            // Add search parameters only if they have values
            if (title) parameters.append("title", title);
            if (director) parameters.append("director", director);
            if (genre) parameters.append("genre", genre);
            if (ageRating) parameters.append("age_rating", ageRating);
            if (duration) parameters.append("duration", duration);
            if (favourite) parameters.append("favourite", favourite);
            if (watched) parameters.append("watched", watched);
            if (releaseYear) parameters.append("release_year", releaseYear);
            if (movieType) parameters.append("type", movieType);
            if (topic) parameters.append("topic", topic);
            if (documentarian) parameters.append("documentarian", documentarian);
            if (isAnimated) parameters.append("is_animated", isAnimated);
            if (moralLesson) parameters.append("moral_lesson", moralLesson);
            if (parentalAppeal) parameters.append("parental_appeal", parentalAppeal);

            setParams(parameters); // Update the search query parameters
        }
    };
    const clearFields = () => {
        setTitle("");
        setDirector("");
        setGenre("");
        setReleaseYear("");
        setDuration("");
        setWatched(""); // Reset to "All"
        setFavourite("");
        setIsAnimated("");
        setAgeRating("");
        setMovieType("movie"); // Reset to default type
        setTopic(""); // Clear documentary-specific field
        setDocumentarian("");
        setMoralLesson(""); // Clear kids' movie-specific field
        setParentalAppeal("");
    };


    return (
        <div className="text-l">
            <form className="space-y-1" onSubmit={handleSubmit}>
                {/* Movie Type Selection (Only editable when adding new movie) */}
                {!updating ? (
                    <div>
                        <label htmlFor="movieType">Movie Type:</label>
                        <select
                            className="form-element"
                            id="movieType"
                            value={movieType}
                            onChange={(e) => setMovieType(e.target.value)}
                        >
                            {action === "search" && <option value="all">All</option>}
                            <option value="movie">Regular Movie</option>
                            <option value="documentary">Documentary</option>
                            <option value="kidMovie">Kids Movie</option>
                        </select>
                    </div>
                ) : (
                    <div>
                        <label htmlFor="movieType">Movie Type:</label>
                        <span className="form-element">{movieType}</span>
                    </div>
                )}



                {/* Movie Title */}
                <div>
                    <label htmlFor="title">Movie Title:</label>
                    <input className="form-element" type="text" id="title" value={title} onChange={(e) => setTitle(e.target.value)} required={action === "add"} />
                </div>

                {/* Director */}
                <div>
                    <label htmlFor="director">Director:</label>
                    <input className="form-element" type="text" id="director" value={director} onChange={(e) => setDirector(e.target.value)} required={action === "add"} />
                </div>

                {/* Genre - Accepts a comma-separated list of genres */}
                <div>
                    <label htmlFor="genre">Genre:</label>
                    <input className="form-element w-80" placeholder="Genres must be seperated by commas" type="text" id="genre" value={genre} onChange={(e) => setGenre(e.target.value)} required={action === "add"} />
                </div>

                {/* Release Year */}
                <div>
                    <label htmlFor="releaseYear">Release Year:</label>
                    <input
                        className="form-element"
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
                        className="form-element"
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
                    {action === "search" ? (
                        // Render a select dropdown if the action is "search"
                        <select
                            className="form-element" id="watched" value={watched} onChange={(e) => setWatched(e.target.value)}
                        >
                            <option value="">Any</option>
                            <option value="true">Yes</option>
                            <option value="false">No</option>
                        </select>
                    ) : (
                        // Render a checkbox if the action is not "search"
                        <input className="form-element w-6 h-5" type="checkbox" id="watched" checked={watched} onChange={() => setWatched(!watched)} // Toggle the isAnimated state
                        />
                    )}
                </div>

                {/* Favourite checkbox */}
                <div>
                    <label htmlFor="favourite">Favourite:</label>
                    {action === "search" ? (
                        // Render a select dropdown if the action is "search"
                        <select
                            className="form-element" id="favourite" value={favourite} onChange={(e) => setFavourite(e.target.value)}
                        >
                            <option value="">Any</option>
                            <option value="true">Yes</option>
                            <option value="false">No</option>
                        </select>
                    ) : (
                        // Render a checkbox if the action is not "search"
                        <input className="form-element w-6 h-5" type="checkbox" id="favourite" checked={favourite} onChange={() => setFavourite(!favourite)}
                        />
                    )}
                </div>

                {/* Is Animated checkbox */}
                <div>
                    <label htmlFor="isAnimated">Is Animated:</label>
                    {action === "search" ? (
                        // Render a select dropdown if the action is "search"
                        <select
                            className="form-element" id="isAnimated" value={isAnimated} onChange={(e) => setIsAnimated(e.target.value)}
                        >
                            <option value="">Any</option>
                            <option value="true">Yes</option>
                            <option value="false">No</option>
                        </select>
                    ) : (
                        // Render a checkbox if the action is not "search"
                        <input className="form-element w-6 h-5" type="checkbox" id="isAnimated" checked={isAnimated} onChange={() => setIsAnimated(!isAnimated)} // Toggle the isAnimated state
                        />
                    )}
                </div>

                {/* Age Rating */}
                <div>
                    <label htmlFor="ageRating">Age Rating:</label>
                    <input
                        className="form-element"
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
                                className="form-element"
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
                                className="form-element"
                                type="text"
                                id="documentarian"
                                value={documentarian}
                                onChange={(e) => setDocumentarian(e.target.value)}
                                required={action === "add"}

                            />
                        </div>
                    </>
                )}
                {/* Display these fields only if movie type is kids movie */}
                {movieType === "kidMovie" && (
                    <>
                        <div>
                            <label htmlFor="moralLesson">Moral Lesson:</label>
                            <input
                                className="form-element"
                                type="text"
                                id="moralLesson"
                                value={moralLesson}
                                onChange={(e) => setMoralLesson(e.target.value)}
                                required={action === "add"}
                            />
                        </div>
                        <div>
                            <label htmlFor="parentalAppeal">Parental Appeal:</label>
                            <input className="form-element" type="number"
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
                {/* Display different button text based on the context */}
                <div className="flex flex-row space-x-6">
                    <button className="btn-primary" type="submit">{updating ? "Update" : action === "add" ? "Add Movie" : "Search Movie"}</button>
                    <button className="btn-primary" onClick={clearFields} type="button">Clear Fields</button>
                </div>

            </form>
        </div>
    );
};

export default EditingMovieRecord;
