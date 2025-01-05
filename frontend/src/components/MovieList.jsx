import React from "react";

const MovieList = ({ movies, updateMovie, updateCallback }) => {
    const onDelete = async (id) => {
        try {
            const options = {
                method: "DELETE"
            }
            const response = await fetch(`http://127.0.0.1:5000/delete_movie/${id}`, options)
            if (response.status === 200) {
                updateCallback()
            } else {
                console.error("Failed to delete")
            }
        } catch (error) {
            alert(error)
        }
    }
    return (
        <div>
            <h2>Movies</h2>
            <table>
                <thead>
                    {/* Table Header: Defines columns for movie details */}
                    <tr>
                        <th>Type</th>
                        <th>Movie Title</th>
                        <th>Director</th>
                        <th>Genre</th>
                        <th>Release Year</th>
                        <th>Duration</th>
                        <th>Favourite</th>
                        <th>Animated</th>
                        <th>Watched</th>
                        <th>Age Rating</th>

                        {/* Additional columns for documentaries */}
                        {movies.some(movie => movie.type === "documentary") && (
                            <>
                                <th>Topic</th>
                                <th>Documentarian</th>
                            </>
                        )}
                    </tr>
                </thead>
                <tbody>
                    {/* Loop over movies and display movie details */}
                    {movies.map((movie) => (
                        <tr key={movie.movieId}>
                            {/* Display basic movie details */}
                            <td>{movie.type}</td>
                            <td>{movie.title}</td>
                            <td>{movie.director}</td>
                            <td>{movie.genre.join(", ")}</td>
                            <td>{movie.releaseYear}</td>
                            <td>{movie.duration}</td>
                            <td>{movie.favourite ? "Yes" : "No"}</td>
                            <td>{movie.isAnimated ? "Yes" : "No"}</td>
                            <td>{movie.watched ? "Yes" : "No"}</td>
                            <td>{movie.ageRating}</td>

                            {/* Render documentary-specific information */}
                            {movie.type === "documentary" && (
                                <>
                                    <td>{movie.topic}</td>
                                    <td>{movie.documentarian}</td>
                                </>
                            )}
                            <td>
                                <button onClick={() => updateMovie(movie)}>Update</button>
                                <button onClick={() => onDelete(movie.movieId)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default MovieList;
