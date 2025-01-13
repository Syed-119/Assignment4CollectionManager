import { useState, useEffect } from "react";
import EditingMovieRecord from "./components/EditingMovieRecord"; // Component to add/search movies
import MovieList from "./components/MovieList"; // Component to display the list of movies
import MovieYearChart from "./components/MovieYearChart"; // Component to display the movie chart

import "./App.css"; // App's CSS

function App() {
  const [allMovies, setAllMovies] = useState([]);
  const [movies, setMovies] = useState([]); // Movies state to store the list of movies
  const [currentMovie, setCurrentMovie] = useState({}); // State for the currently selected movie for update
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [params, setParams] = useState(""); // Query parameters for movie search
  const [activeTab, setActiveTab] = useState("Movies"); // State for active tab (either "Movies" or "Graph")

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

  const fetchAllMovies = async () => {
    const response = await fetch('http://127.0.0.1:5000/search_movies');
    const data = await response.json();
    setAllMovies(data.movies || []);  // Make sure 'allMovies' is the correct property
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
    fetchMovies(params);
  };

  // Fetch movies and all movies when the component mounts
  useEffect(() => {
    fetchMovies();
    fetchAllMovies();
  }, []);

  // Fetch movies when the search params change
  useEffect(() => {
    fetchMovies(params); // Trigger search whenever params change
  }, [params]);

  return (
    <>
      <div className="bg-black min-h-screen">
        <h1 className="flex items-center justify-center h-16 font-bold text-2xl text-white">MOVIE COLLECTION MANAGER</h1>

        <div className="flex flex-row items-start space-x-8 mb-16">
          {/* Box for Adding a Movie */}
          <div className="bg-blue-900 text-white p-6 rounded-md shadow-md w-1/2">
            <h2 className="text-xl font-bold mb-4">Add a Movie</h2>
            <EditingMovieRecord action="add" existingMovie={currentMovie} updateCallback={onUpdate} />
          </div>
          {/* Box for Searching a Movie */}
          <div className="bg-blue-900 text-white p-6 rounded-md shadow-md w-1/2">
            <h2 className="text-xl font-bold mb-4">Search Movies</h2>
            <EditingMovieRecord action="search" params={params} setParams={setParams} updateCallBack={onUpdate} />
          </div>
        </div>

        {/* Modal for editing a movie */}
        {isModalOpen && (
          <div className="modal">
            <div className="modal-content text-white">
              <span className="close" onClick={closeModal}>&times;</span>
              <EditingMovieRecord action="add" existingMovie={currentMovie} updateCallback={onUpdate} />
            </div>
          </div>
        )}

        {/* Tab Navigation for Movies and Graph (Right above the Movie List) */}
        <div className="flex justify-center space-x-4 mb-6">
          <button
            className={`btn-primary ${activeTab === "Movies" ? "bg-green-700" : "bg-blue-900"}`}
            onClick={() => setActiveTab("Movies")}
          >
            Movies
          </button>
          <button
            className={`btn-primary ${activeTab === "Graph" ? "bg-green-700" : "bg-blue-900"}`}
            onClick={() => setActiveTab("Graph")}
          >
            By Year Chart
          </button>
        </div>

        {/* Conditional Rendering Based on Active Tab */}
        <div className="bg-blue-900 text-white p-6 rounded-md shadow-md w-full">
          {activeTab === "Movies" ? (
            <MovieList movies={movies} updateMovie={openEditModal} updateCallBack={onUpdate} />
          ) : (
            // Display the graph tab content
            <div className="bg-black text-white p-6 rounded-md shadow-md w-full mb-8">
              <MovieYearChart allMovies={allMovies} />
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default App;
