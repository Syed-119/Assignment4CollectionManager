import React, { useState } from "react";

const MovieList = ({ movies, updateMovie, updateCallback }) => {
    const [currentPage, setCurrentPage] = useState(1); // State to track the current page for pagination
    const moviesPerPage = 6; // The number of movies displayed per page

    // Calculate the range of movies to display on the current page
    const indexOfLastMovie = currentPage * moviesPerPage;
    const indexOfFirstMovie = indexOfLastMovie - moviesPerPage;
    const currentMovies = movies.slice(indexOfFirstMovie, indexOfLastMovie);

    // Total number of pages based on the movie count and movies per page
    const totalPages = Math.ceil(movies.length / moviesPerPage);

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
                {currentMovies.map((movie) => (
                    <div key={movie.movieId} className="bg-gray-800 p-4 rounded-lg shadow-md">
                        {/* Display common movie details */}
                        <h3 className="text-xl font-bold mb-2">{movie.title}</h3> {/* Movie title */}
                        <p><strong>Type:</strong> {movie.type}</p> {/* Type of the movie (e.g., documentary, kidMovie) */}
                        <p><strong>Director:</strong> {movie.director}</p> {/* Director's name */}
                        <p><strong>Genre:</strong> {movie.genre.join(", ")}</p> {/* List of genres, joined by commas */}
                        <p><strong>Release Year:</strong> {movie.releaseYear}</p> {/* Release year of the movie */}
                        <p><strong>Duration:</strong> {movie.duration}</p> {/* Duration in minutes */}
                        <p><strong>Favourite:</strong> {movie.favourite ? "Yes" : "No"}</p> {/* Whether it's marked as favourite */}
                        <p><strong>Animated:</strong> {movie.isAnimated ? "Yes" : "No"}</p> {/* Is it animated */}
                        <p><strong>Watched:</strong> {movie.watched ? "Yes" : "No"}</p> {/* Has it been watched */}
                        <p><strong>Age Rating:</strong> {movie.ageRating}</p> {/* Age rating of the movie */}

                        {/* Additional fields specific to documentaries */}
                        {movie.type === "documentary" && (
                            <>
                                <p><strong>Topic:</strong> {movie.topic}</p> {/* Topic of the documentary */}
                                <p><strong>Documentarian:</strong> {movie.documentarian}</p> {/* Name of the documentarian */}
                            </>
                        )}

                        {/* Additional fields specific to kids' movies */}
                        {movie.type === "kidMovie" && (
                            <>
                                <p><strong>Moral Lesson:</strong> {movie.moralLesson}</p> {/* Moral lesson conveyed by the movie */}
                                <p><strong>Parental Appeal:</strong> {movie.parentalAppeal}</p> {/* Appeal score for parents */}
                            </>
                        )}

                        {/* Action Buttons for Update and Delete */}
                        <div className="mt-4 flex space-x-2">
                            <button className="btn-primary" onClick={() => updateMovie(movie)}>Update</button> {/* Trigger update logic */}
                            <button className="btn-primary" onClick={() => onDelete(movie.movieId)}>Delete</button> {/* Trigger delete logic */}
                        </div>
                    </div>
                ))}
            </div>

            {/* Pagination Controls */}
            <div className="flex justify-center mt-6 space-x-4">
                <button
                    className="btn-primary"
                    onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))} // Go to the previous page
                    disabled={currentPage === 1}
                >
                    Previous
                </button>
                <span className="text-lg">{`Page ${currentPage} of ${totalPages}`}</span> {/* Display current page out of total pages */}
                <button
                    className="btn-primary"
                    onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))} // Go to the next page
                    disabled={currentPage === totalPages} // Disable if already on the last page
                >
                    Next
                </button>

                {/* Total number of movies */}
                <div className="absolute right-4 text-white font-bold">
                    Total Movies: {currentMovies.length}
                </div>
            </div>
        </div>
    );
};

export default MovieList;
