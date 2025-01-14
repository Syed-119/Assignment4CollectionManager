import React, { useState } from "react";

const MovieList = ({ movies, updateMovie, updateCallback }) => {
    const [currentPage, setCurrentPage] = useState(1); // State to track the current page for pagination
    const moviesPerPage = 6; // The number of movies displayed per page

    const validMovies = Array.isArray(movies) ? movies.filter(movie => movie !== null && typeof movie === "object") : [];

    // Calculate the range of movies to display on the current page
    const indexOfLastMovie = currentPage * moviesPerPage;
    const indexOfFirstMovie = indexOfLastMovie - moviesPerPage;
    const currentMovies = movies.slice(indexOfFirstMovie, indexOfLastMovie);

    // Total number of pages based on the movie count and movies per page
    const totalPages = Math.max(1, Math.ceil(validMovies.length / moviesPerPage));

    // Safely set the current page within valid range
    const setPageSafely = (newPage) => {
        setCurrentPage(Math.max(1, Math.min(newPage, totalPages)));
    };

    // Function to handle deletion of a movie
    const onDelete = async (id) => {
        try {
            const options = { method: "DELETE" };
            const response = await fetch(`http://127.0.0.1:5000/delete_movie/${id}`, options); // API call to delete movie
            if (response.status === 200) {
                alert("Movie Deleted Successfully"); // Alert user on successful deletion
                updateCallback(); // Notify parent component to refresh the movie list
            } else {
                console.error("Failed to delete");
            }
        } catch (error) {
            console.error("Failed to delete");
        }
    };

    return (
        <div className="text-white">
            {/* Header Section */}
            <h2 className="text-2xl font-bold mb-4">Movies</h2>

            {/* Movie List Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {/* Iterate over the movies for the current page */}
                {currentMovies.length > 0 ? (
                    currentMovies.map((movie) => (
                        movie && (
                            <div key={movie.movieId || Math.random()} className="bg-gray-800 p-4 rounded-lg shadow-md">
                                <h3 className="text-xl font-bold mb-2">{movie.title || "Untitled Movie"}</h3>
                                <p><strong>Type:</strong> {movie.type || "N/A"}</p>
                                <p><strong>Director:</strong> {movie.director || "Unknown"}</p>
                                <p><strong>Genre:</strong> {movie.genre?.join(", ") || "None"}</p>
                                <p><strong>Release Year:</strong> {movie.releaseYear || "N/A"}</p>
                                <p><strong>Duration:</strong> {movie.duration || "N/A"}</p>
                                <p><strong>Favourite:</strong> {movie.favourite ? "Yes" : "No"}</p>
                                <p><strong>Animated:</strong> {movie.isAnimated ? "Yes" : "No"}</p>
                                <p><strong>Watched:</strong> {movie.watched ? "Yes" : "No"}</p>
                                <p><strong>Age Rating:</strong> {movie.ageRating || "N/A"}</p>

                                {movie.type === "documentary" && (
                                    <>
                                        <p><strong>Topic:</strong> {movie.topic || "N/A"}</p>
                                        <p><strong>Documentarian:</strong> {movie.documentarian || "Unknown"}</p>
                                    </>
                                )}
                                {movie.type === "kidMovie" && (
                                    <>
                                        <p><strong>Moral Lesson:</strong> {movie.moralLesson || "N/A"}</p>
                                        <p><strong>Parental Appeal:</strong> {movie.parentalAppeal || "N/A"}</p>
                                    </>
                                )}

                                <div className="mt-4 flex space-x-2">
                                    <button className="btn-primary" onClick={() => updateMovie(movie)}>Update</button>
                                    <button className="btn-primary" onClick={() => onDelete(movie.movieId)}>Delete</button>
                                </div>
                            </div>
                        )
                    ))
                ) : (
                    <p className="text-white">No movies available to display.</p>
                )}
            </div>

            {/* Pagination Controls */}
            <div className="flex justify-center mt-6 space-x-4">
                <button
                    className="btn-primary"
                    onClick={() => setPageSafely(currentPage - 1)} // Go to the previous page
                    disabled={currentPage === 1}
                >
                    Previous
                </button>
                <span className="text-lg">{`Page ${currentPage} of ${totalPages}`}</span> {/* Display current page out of total pages */}
                <button
                    className="btn-primary"
                    onClick={() => setPageSafely(currentPage + 1)} // Go to the next page
                    disabled={currentPage === totalPages} // Disable if already on the last page
                >
                    Next
                </button>
            </div>
            {/* Total number of movies */}
            <div className="absolute right-4 text-white font-bold">
                Total Movies: {validMovies.length}
            </div>
        </div>
    );
};

export default MovieList;
