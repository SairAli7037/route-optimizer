from django.urls import path
from .views import optimize_route, route_map
from .views import optimize_route


urlpatterns = [
    path(
        "optimize-route/",
        optimize_route,
        name="optimize-route"
    ),
      path(
        "map/",
        route_map,
        name="route-map"
    ),
]