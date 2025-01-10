import React from "react";
import { Bar } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js";


ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const MovieYearChart = ({ fetchMovies, movies }) => {
    const yearCounts = movies.reduce((acc, movie) => {
        acc[movie.releaseYear] = (acc[movie.releaseYear] || 0) + 1;
        return acc;
    }, {});





    const data = {
        labels: Object.keys(yearCounts),
        datasets: [
            {
                label: "All Movies by Year",
                data: Object.values(yearCounts),
                backgroundColor: "rgba(54, 162, 235, 0.6)",
                borderColor: "blue",
                borderWidth: 1,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: "top",
            },
            title: {
                display: true,
                text: "Movies by Release Year",
            },
        },
    };

    return <Bar data={data} options={options} />;
};

export default MovieYearChart;
