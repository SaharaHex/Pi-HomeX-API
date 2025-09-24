const express = require("express");
const cors = require("cors"); // Optional
const app = express();

app.use(cors()); // Optional for frontend access

app.get('/', (req, res) => res.status(200).json({ result: 'Success from Pi-HomeX-API!' }));

// Modular routes
app.use('/timezone', require('./routes/timezone'));
app.use('/timezones', require('./routes/timezones'));
app.use('/weather', require('./routes/weather'));
app.use("/raspberry", require("./routes/raspberry"));
app.use('/help', require('./routes/help'));

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
