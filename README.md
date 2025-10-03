# Pi-HomeX-API
This is a Raspberry Pi project that creates local APIs to retrieve weather data and RSS feeds, displaying the results on a 792×272 E-paper display.

The project is divided into three components:

express_api :

Built with Express (Node.js), this service fetches weather data from api.open-meteo.com and api.sunrise-sunset.org, and also provides Raspberry Pi system diagnostics.

flask_api :

Developed using Flask (Python), this API retrieves RSS feeds and returns curated News and Tech items.

waveshare_e-paper : 

A Python script that updates the Waveshare E-paper display with the latest weather data.
