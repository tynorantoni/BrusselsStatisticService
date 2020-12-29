# BrusselsStatisticService

## Microservice project written in python.
## Consisting of 5 working separately microservices listed below.

* All microservices are connected to PostgreSQL Database.
* All microservices are 'micro-flask-aplications' with 'ping' endpoint which is used by Health Check Service to maintaining their	state of life.
* All microservices are containerized with Docker, all of them are deployed by Travis CI to AWS ECR.

#### 1. [Brussels Statistic Service (BSS)](https://github.com/tynorantoni/BrusselsStatisticService)
- Main task of this app is cyclical sending request to Brussels Bicycle API, in response BSS is taking daily data about number of cyclists riding in Brussels and insert it into database.
#### 2. [Krakow Statistic Service (KSS)](https://github.com/tynorantoni/KrakowStatisticService)
- Similar to BSS, main goal is to receive data from the official krakow page with bicycle data. However, due to the lack of API endpoint KSS is using Selenium to web-scrape data directly from daily counters and insert it into DB.
#### 3. [Weather Check Service (WCS)](https://github.com/tynorantoni/WeatherCheckService)
- Service taking data from AccuWeather API every hour.
#### 4. [Health Check Service (HCS)](https://github.com/tynorantoni/HealthCheckService)
- As mentioned above - only task is to check state of the other services. 
#### 5. [Data Analyzer Service (DAS)](https://github.com/tynorantoni/DataAnalyzerService)
- Also, a flask micro-app, with endpoints responses data like - analyzed weather data, processed statistic data (with Pandas and NumPy) from bicycle counters and health check statuses.

## [Front End Layer](https://github.com/tynorantoni/Front-End-Layer-of-United-Services)
- Django App with Tailwinds CSS as layout which aggregates all this data and show it in accessible and readable format.
- Charts are maintained by chart.js library.
