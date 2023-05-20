window.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#weather-form');
    const weatherInfo = document.querySelector('#weather-info');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const locationInput = document.querySelector('#location');
        const location = locationInput.value;
        const weatherData = await getWeather(location);
        displayWeatherInfo(weatherData);
    });

    async function getWeather(location) {
        const response = await fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `location=${encodeURIComponent(location)}`,
        });
        const data = await response.text();
        const parser = new DOMParser();
        const html = parser.parseFromString(data, 'text/html');
        const weatherInfo = html.querySelector('#weather-info');
        return weatherInfo.innerHTML;
    }

    function displayWeatherInfo(weatherData) {
        weatherInfo.innerHTML = weatherData;
    }
});
