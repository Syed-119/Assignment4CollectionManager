import { useState, useEffect } from 'react';
import AddingMovieRecord from './components/AddingMovieRecord'; // Component to add/search movies
import MovieList from './components/MovieList'; // Component to display the list of movies

import './App.css'; // App's CSS

function App() {
  const [movies, setMovies] = useState([]); // Movies state to store the list of movies
  const [currentMovie, setCurrentMovie] = useState({}); // State for the currently selected movie for update
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [params, setParams] = useState("");

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

  const fetchMovies = async (params) => {
    try {
      // Ensure params is a valid URLSearchParams object
      const queryString = params ? params.toString() : "";

      // Send the GET request to the backend
      const response = await fetch(`http://127.0.0.1:5000/search_movies?${queryString}`, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      // Process the JSON response
      const data = await response.json();
      console.log("Movies to set:", data.movies);
      setMovies(data.movies); // Assuming setMovies is accessible in the scope

      // Optional: Return data for further use
      return data.movies;
    } catch (error) {
      console.error("Error fetching movies:", error);
    }
  };

  // Callback after updating a movie
  const onUpdate = () => {
    closeModal();
    fetchMovies();
  };

  // Fetch movies whenever the params change
  useEffect(() => {
    if (params) {
      fetchMovies(params);
    }
  }, [params]);

  return (
    <>
      <AddingMovieRecord action="add" existingMovie={currentMovie} updateCallback={onUpdate} />

      {isModalOpen && <div className="modal">
        <div className="modal-content">
          <span className="close" onClick={closeModal}>&times;</span>
          <AddingMovieRecord action="add" existingMovie={currentMovie} updateCallback={onUpdate} />
        </div>
      </div>
      }

      <br />

      {/* Form to search movies */}
      <AddingMovieRecord
        action="search"
        params={params}
        setParams={setParams}
        updateCallBack={onUpdate}
      />

      {/* Display the list of movies */}
      <MovieList
        movies={movies}
        updateMovie={openEditModal}
        updateCallBack={onUpdate}
      />
    </>
  );
}

export default App;
