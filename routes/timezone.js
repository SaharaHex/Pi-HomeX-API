const express = require("express");
const router = express.Router();

/**
 * Returns current date and time in specified timezone.
 * Validates against supported IANA timezones.
 * Defaults to Europe/London if none provided. 
 * Example: GET
 * /timezone
 * /timezone?tz=America/Europe/London
 * /timezone?tz=America/Mexico_City
 */

router.get("/", (req, res) => {
  const requestedTZ = req.query.tz || "Europe/London"; // Default to UK
  const supportedTimezones = Intl.supportedValuesOf("timeZone");

  const result = {
    date: null,
    time: null,
    timezone: requestedTZ,
    errors: []
  };

  // Validate timezone
  if (!supportedTimezones.includes(requestedTZ)) {
    const fallback = new Date();

    result.date = `${String(fallback.getDate()).padStart(2, '0')}/${String(fallback.getMonth() + 1).padStart(2, '0')}/${fallback.getFullYear()}`;
    result.time = `${String(fallback.getHours()).padStart(2, '0')}:${String(fallback.getMinutes()).padStart(2, '0')}:${String(fallback.getSeconds()).padStart(2, '0')}`;
    result.timezone = "LocalTime";
    result.errors.push(`Invalid timezone: "${requestedTZ}". Fallback to system time.`);
    return res.status(200).json(result);
  }

  try {
    // Create a date string in the target timezone
    const now = new Date();

    const options = {
      timeZone: requestedTZ,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour12: false
    };

    const localeString = now.toLocaleString("en-GB", options);
    const [datePart, timePart] = localeString.split(", ");

    result.date = datePart;
    result.time = timePart;
  } catch (error) {
    const fallback = new Date();

    result.date = `${String(fallback.getDate()).padStart(2, '0')}/${String(fallback.getMonth() + 1).padStart(2, '0')}/${fallback.getFullYear()}`; // Months are 0-indexed
    result.time = `${String(fallback.getHours()).padStart(2, '0')}:${String(fallback.getMinutes()).padStart(2, '0')}:${String(fallback.getSeconds()).padStart(2, '0')}`;
    result.timezone = "LocalTime";
    result.errors.push(`Failed to format time for timezone "${requestedTZ}"`);
  }

  res.status(200).json(result);
});

module.exports = router;
