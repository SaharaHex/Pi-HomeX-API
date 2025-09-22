const express = require("express");
const router = express.Router();

/**
 * Fetches sunrise/sunset, current weather, hourly forecast for rest of day, and local time.
 * Returns structured JSON.
 * Example: GET
 * /weather
 * /weather?lat=51.50&lon=-0.12&timezone=Europe/London
 * /weather?lat=19.43&lon=-99.13&timezone=America/Mexico_City
 */

function interpretWeatherCode(code) {
  if (code === 0) return "Clear";
  if (code >= 1 && code <= 3) return "Cloudy";
  if (code >= 45 && code <= 48) return "Fog";
  if (code >= 51 && code <= 67) return "Rain";
  if (code >= 71 && code <= 77) return "Snow";
  if (code >= 80 && code <= 82) return "Rain Showers";
  if (code >= 85 && code <= 86) return "Snow Showers";
  if (code >= 95 && code <= 99) return "Thunderstorm";
  return "Unknown";
}

async function getEnvironmentSnapshot(lat, lon, timezone) {
  // 🕰️ Local Raspberry Pi Time
  const now = new Date();
  const formattedTime = {
    time: `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`,
    date: `${String(now.getDate()).padStart(2, '0')}/${String(now.getMonth() + 1).padStart(2, '0')}/${now.getFullYear()}`
  };

  const forecastData = {
    timezone: timezone,
    LATITUDE: lat, 
    LONGITUDE: lon
  };

  const snapshot = {
    local_pi_time: formattedTime,
    forecast_data: forecastData,
    sunrise_sunset: null,
    weather: null,
    forecast_next: [],
    forecast_end_time: null,
    forecast_remaining_hours : null,
    errors: []
  };

  // 🌅 Sunrise/Sunset
  try {
    const dateStr = now.toISOString().split('T')[0]; // "2025-09-17"
    const sunRes = await fetch(`https://api.sunrise-sunset.org/json?lat=${lat}&lng=${lon}&date=${dateStr}&tzid=${timezone}`);
    const sunData = await sunRes.json();
    snapshot.sunrise_sunset = {
      sunrise: sunData.results.sunrise,
      sunset: sunData.results.sunset
    };
  } catch (err) {
    snapshot.errors.push({
      source: "sunrise-sunset.org",
      message: err.message || "Failed to fetch sunrise/sunset"
    });
  }

  // 🌡️ Current Weather + 5-Hour Forecast
  try {
    const weatherRes = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&hourly=temperature_2m,wind_speed_10m,relative_humidity_2m,weathercode&current_weather=true&forecast_days=1&timezone=${timezone}`);
    const weatherData = await weatherRes.json();

    let currentTime = null;
    // Current weather
    if (weatherData.current_weather) {
      currentTime = new Date(weatherData.current_weather.time);
      let closestIndex = -1;
      let smallestDiff = Infinity;

      weatherData.hourly.time.forEach((t, i) => {
        const hourlyTime = new Date(t);
        const diff = Math.abs(hourlyTime - currentTime);
        if (diff < smallestDiff) {
          smallestDiff = diff;
          closestIndex = i;
        }
      });

      snapshot.weather = {
        time: currentTime.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }), // e.g., "19:00",
        temperature_celsius: weatherData.current_weather.temperature,
        wind_speed_kmh: weatherData.current_weather.windspeed,
        humidity_percent: closestIndex !== -1 // Match Closest Hour Instead of Exact Time
          ? weatherData.hourly.relative_humidity_2m[closestIndex]
          : null,
        condition: closestIndex !== -1 // Match Closest Hour Instead of Exact Time
          ? interpretWeatherCode(weatherData.hourly.weathercode[closestIndex])
          : "Unknown"
      };
    }    

    // 🌤️ Remaining hours of today forecast
    const currentTimeMs = currentTime.getTime();
    const endOfDay = new Date(currentTime);
    endOfDay.setHours(23, 59, 59, 999);
    const endOfDayMs = endOfDay.getTime();

    weatherData.hourly.time.forEach((timestamp, index) => {
      const dateObj = new Date(timestamp);
      const timeMs = dateObj.getTime();

      if (timeMs > currentTimeMs && timeMs <= endOfDayMs) {
        snapshot.forecast_next.push({
          time: dateObj.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }), // e.g., "19:00"
          temperature_celsius: weatherData.hourly.temperature_2m[index],
          wind_speed_kmh: weatherData.hourly.wind_speed_10m[index],
          humidity_percent: weatherData.hourly.relative_humidity_2m[index],
          condition: interpretWeatherCode(weatherData.hourly.weathercode[index])
        });
      }
    });
    
    snapshot.forecast_end_time = "23:00";
    snapshot.forecast_remaining_hours = snapshot.forecast_next.length;

  } catch (err) {
    snapshot.errors.push({
      source: "open-meteo.com",
      message: err.message || "Failed to fetch weather/forecast data"
    });
  }

  return snapshot;
}

router.get('/', async (req, res) => { // Default is UK London
  const lat = req.query.lat || "51.50"; // Latitude 
  const lon = req.query.lon || "-0.12";  // Longitude 
  const timezone = req.query.timezone || "Europe/London";

  const snapshot = await getEnvironmentSnapshot(lat, lon, timezone);
  res.status(200).json(snapshot);
});

module.exports = router;
