import { useEffect, useState } from 'react'
import AddingMovieRecord from './components/AddingMovieRecord'  // Component to add new movies
import MovieList from './components/MovieList'  // Component to display the list of movies

import './App.css'  // App's CSS


function App() {
  const [movies, setMovies] = useState([])  // State to store movies

  useEffect(() => {
    fetchMovies()  // Fetch movies on initial render
  }, [])

  // Fetch movies from the backend
  const fetchMovies = async () => {
    const response = await fetch("http://127.0.0.1:5000/search_movies")
    const data = await response.json()
    setMovies(data.movies)  // Update state with fetched movies
    console.log(data.movies)  // Log movies (for debugging)
  };

  return (
    <>
      {/* <MovieList movies={movies} />  Display movies */}
      <AddingMovieRecord action={"add"} />  {/* Form to add new movies */}
      <br></br>
      <AddingMovieRecord action={"search"} />
    </>
  )
}

export default App
