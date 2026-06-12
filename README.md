# Route Optimizer
Repository: https://github.com/SairAli7037/route-optimizer

## Project Overview

This project solves the Route Optimization assessment. Given a start and destination location within the United States, the system generates a driving route, identifies fuel stations near the route, and selects cost-effective fuel stops while respecting a maximum vehicle range of 500 miles.

The application calculates the total fuel cost assuming a fuel efficiency of 10 MPG and visualizes the optimized route and fuel stops on an interactive map.


## Features

- Route generation using OpenRouteService
- City name based route input
- Automatic geocoding
- Fuel station filtering near route
- Fuel stop optimization
- Total fuel cost calculation
- Interactive map visualization
- Error handling for invalid routes

## Assumptions

- Vehicle range: 500 miles
- Fuel efficiency: 10 MPG
- Fuel prices sourced from provided dataset

## Optimization Logic

1. Generate route between origin and destination.
2. Sample route points.
3. Find fuel stations near the route.
4. Order stations along the route.
5. Split journey into 500-mile reachable windows.
6. Select the lowest-cost fuel station within each window.
7. Calculate total fuel cost.

## Architecture

```text
User Input
      |
      v
GeocodingService
      |
      v
RoutingService
      |
      v
StationService
      |
      v
FuelOptimizer
      |
      v
CostService
      |
      v
Map Visualization
```

## Technologies Used

* Python 3.12
* Django
* OpenRouteService API
* SQLite
* Leaflet.js
* OpenStreetMap
* HTML/CSS/JavaScript


## How to Run

1. Clone the repository

```bash
git clone https://github.com/SairAli7037/route-optimizer.git
cd route-optimizer
```

2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add:

```env
ORS_API_KEY=your_openrouteservice_api_key
```

5. Run migrations

```bash
python manage.py migrate
```

6. Start the development server

```bash
python manage.py runserver
```

7. Open:

```text
http://127.0.0.1:8000/api/map/
```



## Performance Considerations

- Fuel stations are loaded into the database once.
- Route API is called only once per optimization request.
- Candidate stations are filtered spatially before optimization.
- Route ordering is computed using sampled route points.



## Screenshots
## Route Optimization Result

![Route Map](screenshots/route-map.png)

## Fuel Stops

![Fuel Stops](screenshots/Fuel-stops1.png)
![Fuel Stops](screenshots/Fuel-stops2.png)

## Architecture

![Architecture](screenshots/architecture.png)
