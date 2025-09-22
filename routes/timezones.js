const express = require("express");
const router = express.Router();

/**
 * Returns a list of supported IANA timezones.
 * Example: GET /timezones
 */

router.get("/", (req, res) => {
  try {
    const timezones = Intl.supportedValuesOf("timeZone");
    res.status(200).json({ supported_timezones: timezones });
  } catch (err) {
    res.status(500).json({
      error: "Failed to retrieve supported timezones",
      details: err.message
    });
  }
});

module.exports = router;
