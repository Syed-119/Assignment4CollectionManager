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

// Register necessary Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const MovieYearChart = ({ allMovies }) => {
    // Count movies by their release year
    const yearCounts = allMovies.reduce((acc, movie) => {
        acc[movie.releaseYear] = (acc[movie.releaseYear] || 0) + 1;
        return acc;
    }, {});

    // Prepare the chart data
    const data = {
        labels: Object.keys(yearCounts), // Years on x-axis
        datasets: [
            {
                label: "All Movies by Year",
                data: Object.values(yearCounts), // Movie counts for each year
                backgroundColor: "rgba(54, 162, 235, 0.6)", // Bar color
                borderColor: "blue", // Border color
                borderWidth: 1, // Border width
            },
        ],
    };

    // Chart options for customization
    const options = {
        responsive: true,
        plugins: {
            legend: { position: "top" }, // Position of the legend
            title: {
                display: true,
                text: "Movies by Release Year", // Chart title
            },
        },
    };

    // Render the Bar chart component
    return <Bar data={data} options={options} />;
};

export default MovieYearChart;
