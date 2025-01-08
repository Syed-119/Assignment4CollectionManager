import React, { useState } from "react";

const MovieList = ({ movies, updateMovie, updateCallback }) => {
    const [currentPage, setCurrentPage] = useState(1);
    const moviesPerPage = 6;

    // Calculate the index range for the current page
    const indexOfLastMovie = currentPage * moviesPerPage;
    const indexOfFirstMovie = indexOfLastMovie - moviesPerPage;
    const currentMovies = movies.slice(indexOfFirstMovie, indexOfLastMovie);
    // Pagination controls
    const totalPages = Math.ceil(movies.length / moviesPerPage);

    const onDelete = async (id) => {
        try {
            const options = { method: "DELETE" };
            const response = await fetch(`http://127.0.0.1:5000/delete_movie/${id}`, options);
            if (response.status === 200) {
                alert("Movie Deleted Successfully")
                updateCallback();
            } else {
                console.error("Failed to delete");
            }
        } catch (error) {
            console.error("Failed to delete");
        }
    };

    return (
        <div className="text-white">
            <h2 className="text-2xl font-bold mb-4">Movies</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {currentMovies.map((movie) => (
                    <div key={movie.movieId} className="bg-gray-800 p-4 rounded-lg shadow-md">
                        <h3 className="text-xl font-bold mb-2">{movie.title}</h3>
                        <p><strong>Type:</strong> {movie.type}</p>
                        <p><strong>Director:</strong> {movie.director}</p>
                        <p><strong>Genre:</strong> {movie.genre.join(", ")}</p>
                        <p><strong>Release Year:</strong> {movie.releaseYear}</p>
                        <p><strong>Duration:</strong> {movie.duration}</p>
                        <p><strong>Favourite:</strong> {movie.favourite ? "Yes" : "No"}</p>
                        <p><strong>Animated:</strong> {movie.isAnimated ? "Yes" : "No"}</p>
                        <p><strong>Watched:</strong> {movie.watched ? "Yes" : "No"}</p>
                        <p><strong>Age Rating:</strong> {movie.ageRating}</p>
                        {movie.type === "documentary" && (
                            <>
                                <p><strong>Topic:</strong> {movie.topic}</p>
                                <p><strong>Documentarian:</strong> {movie.documentarian}</p>
                            </>
                        )}
                        {movie.type === "kidMovie" && (
                            <>
                                <p><strong>Moral Lesoon:</strong> {movie.moralLesson}</p>
                                <p><strong>Parental Appeal:</strong> {movie.parentalAppeal}</p>
                            </>
                        )}
                        <div className="mt-4 flex space-x-2">
                            <button className="btn-primary" onClick={() => updateMovie(movie)}>Update</button>
                            <button className="btn-primary" onClick={() => onDelete(movie.movieId)}>Delete</button>
                        </div>
                    </div>
                ))}
            </div>
            {/* Pagination Controls */}
            <div className="flex justify-center mt-6 space-x-4">
                <button
                    className="btn-primary" onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                >Previous</button>
                <span className="text-lg">{`Page ${currentPage} of ${totalPages}`}</span>
                <button className="btn-primary" onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages}
                >Next</button>
            </div>
        </div>
    );
};

export default MovieList;
