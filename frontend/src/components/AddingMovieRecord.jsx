import React, { useState } from "react";

const AddingMovieRecord = () => {
    // State variables to hold form data
    const [title, setTitle] = useState("");
    const [director, setDirector] = useState("");
    const [genre, setGenre] = useState("");
    const [releaseYear, setReleaseYear] = useState("");
    const [duration, setDuration] = useState("");
    const [watched, setWatched] = useState(false);
    const [favourite, setFavourite] = useState(false);
    const [isAnimated, setIsAnimated] = useState(false);
    const [ageRating, setAgeRating] = useState("");
    const [movieType, setMovieType] = useState("movie");  // Default type is "movie"
    const [topic, setTopic] = useState("");  // Specific to documentaries
    const [documentarian, setDocumentarian] = useState("");  // Specific to documentaries

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Prepare the movie record object
        const movieRecord = {
            title,
            director,
            genre: genre.split(",").map((g) => g.trim()),  // Split and clean up the genres
            releaseYear: parseInt(releaseYear, 10),  // Convert to integer
            duration: parseInt(duration, 10),  // Convert to integer
            favourite,
            isAnimated,
            watched,
            ageRating,
            type: movieType,  // Store the selected movie type
            topic,  // Only used for documentaries
            documentarian  // Only used for documentaries
        };

        // Send the movie record to the backend
        const url = "http://127.0.0.1:5000/add_movies";
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(movieRecord),
        };
        const response = await fetch(url, options);

        // Handle the response based on status
        if (response.status !== 201 && response.status !== 200) {
            const data = await response.json();
            alert(data.message);  // Show any error message from the server
        } else {
            // Handle success (could add success message or redirect)
        }
    };

    return (
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
                </select>
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
                            required
                        />
                    </div>
                    <div>
                        <label htmlFor="documentarian">Documentarian:</label>
                        <input
                            type="text"
                            id="documentarian"
                            value={documentarian}
                            onChange={(e) => setDocumentarian(e.target.value)}
                            required
                        />
                    </div>
                </>
            )}

            {/* Movie Title */}
            <div>
                <label htmlFor="title">Movie Title:</label>
                <input
                    type="text"
                    id="title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
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
                    required
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
                    required
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
                    required
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
                    required
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
                    required
                />
            </div>

            {/* Submit Button */}
            <button type="submit">Add Movie</button>
        </form>
    );
};

export default AddingMovieRecord;
