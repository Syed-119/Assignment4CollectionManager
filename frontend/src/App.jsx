import { useState, useEffect } from "react";
import AddingMovieRecord from "./components/AddingMovieRecord"; // Component to add/search movies
import MovieList from "./components/MovieList"; // Component to display the list of movies

import "./App.css"; // App's CSS

function App() {
  const [movies, setMovies] = useState([]); // Movies state to store the list of movies
  const [currentMovie, setCurrentMovie] = useState({}); // State for the currently selected movie for update
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [params, setParams] = useState(""); // Query parameters for movie search

  // Close the modal and reset the current movie
  const closeModal = () => {
    setIsModalOpen(false);
    setCurrentMovie({});
  };

  // Open modal for editing a movie
  const openEditModal = (movie) => {
    if (isModalOpen) return;
    setCurrentMovie(movie);
    setIsModalOpen(true);
  };

  // Fetch movies from the backend
  const fetchMovies = async (params = "") => {
    try {
      const queryString = params instanceof URLSearchParams ? params.toString() : params;
      const response = await fetch(`http://127.0.0.1:5000/search_movies?${queryString}`);
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setMovies(data.movies || []); // Update the movie list
    } catch (error) {
      console.error("Error fetching movies:", error);
    }
  };

  // Callback after updating a movie
  const onUpdate = () => {
    closeModal();
    fetchMovies(params); // Refresh the movie list after update, using the current search params
  };

  // Fetch movies when the page loads
  useEffect(() => {
    fetchMovies(); // Fetch all movies when the component mounts
  }, []);

  // Fetch movies when the search params change
  useEffect(() => {
    fetchMovies(params); // Trigger search whenever params change
  }, [params]);

  return (
    <>
      {/* Form to add a new movie */}
      <AddingMovieRecord action="add" existingMovie={currentMovie} updateCallback={onUpdate} />

      {/* Modal for editing a movie */}
      {isModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <span className="close" onClick={closeModal}>&times;</span>
            <AddingMovieRecord action="add" existingMovie={currentMovie} updateCallback={onUpdate} />
          </div>
        </div>
      )}
      {/* Form to search movies */}
      <AddingMovieRecord action="search" params={params} setParams={setParams} updateCallBack={onUpdate} />

      {/* Display the list of movies */}
      <MovieList movies={movies} updateMovie={openEditModal} updateCallBack={onUpdate} />
    </>
  );
}

export default App;
