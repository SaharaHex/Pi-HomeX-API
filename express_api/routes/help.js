const express = require("express");
const router = express.Router();

/**
 * Provides usage instructions for /weather and /timezone endpoints.
 * Example: GET /help
 */

router.get("/", (req, res) => {
  res.status(200).json({
    endpoints: {
      "/weather": {
        description: "Returns local time, sunrise/sunset, current weather, and hourly forecast for the rest of the day.",
        query_parameters: {
          lat: "Latitude (e.g., 51.50)",
          lon: "Longitude (e.g., -0.12)",
          timezone: "IANA timezone (e.g., Europe/London)"
        },
        examples: [
          "/weather",
          "/weather?lat=51.50&lon=-0.12&timezone=Europe/London",
          "/weather?lat=19.43&lon=-99.13&timezone=America/Mexico_City"
        ],
        data_sources: [
          "Weather data from open-meteo.com",
          "Sunrise and sunset times from api.sunrise-sunset.org"
        ]
      },
      "/timezone": {
        description: "Returns current date and time in specified timezone.",
        query_parameters: {
          tz: "IANA timezone (e.g., America/New_York)"
        },
        examples: [
          "/timezone",
          "/timezone?tz=Europe/London",
          "/timezone?tz=America/Mexico_City"
        ]
      },
      "/timezones": {
        description: "Returns a list of supported IANA timezones.",
        examples: [
          "/timezones"
        ]
      },
      "/raspberry": {
        description: "Returns Raspberry Pi system diagnostics in structured format.",
        examples: [
          "/raspberry"
        ]
      }      
    },
    notes: [
      "All timezones must follow IANA format (e.g., 'Europe/London', not 'GMT+1').",
      "If a timezone is invalid, system time will be used as fallback.",
      "Weather and forecast data are aligned to the specified timezone.",
      "Sunrise/sunset times are calculated based on latitude, longitude, and date."
    ],
    version: "1.0.0",
    author: "SaharaHex"
  });
});

module.exports = router;
