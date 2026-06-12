from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .services.geocoding_service import (
        GeocodingService
    )
import json

from .services.route_optimizer_service import (
    RouteOptimizerService
)

@csrf_exempt
@require_POST
def optimize_route(request):

    try:

        data = json.loads(
            request.body
        )

        start = (
            data["start_lat"],
            data["start_lng"]
        )

        end = (
            data["end_lat"],
            data["end_lng"]
        )

        result = (
            RouteOptimizerService.optimize(
                start,
                end
            )
        )

        return JsonResponse(
            result,
            safe=False
        )

    except Exception as e:

        return JsonResponse(
            {
                "error": str(e)
            },
            status=400
        )
    




def route_map(request):
    
    start_city = request.GET.get(
        "start_city"
    )
    
    end_city = request.GET.get(
        "end_city"
    )

    error_message =None

    try:

        if start_city and end_city:
    
            start_lat, start_lng = (
                GeocodingService.get_coordinates(
                    start_city
                )
            )
        
            end_lat, end_lng = (
                GeocodingService.get_coordinates(
                    end_city
                )
            )
        
        else:
        
            start_lat = 40.7128
            start_lng = -74.0060
        
            end_lat = 34.0522
            end_lng = -118.2437

    except Exception as e:

        print("GEOCODING ERROR:", e)
    
        error_message = (
            "One or both cities not found. "
            "Showing default route."
        )
    
        start_lat = 40.7128
        start_lng = -74.0060
    
        end_lat = 34.0522
        end_lng = -118.2437
        # error_message = "One or both cities not found. Showing default route from New York to Los Angeles."
    

    try:
    
        result = RouteOptimizerService.optimize(
            (
                start_lat,
                start_lng
            ),
            (
                end_lat,
                end_lng
            )
        )
    
    except Exception:
    
        error_message = (
            "Route could not be generated. Showing default route."
        )
    
        result = RouteOptimizerService.optimize(
            (
                40.7128,
                -74.0060
            ),
            (
                34.0522,
                -118.2437
            )
        )
        result["error_message"] = error_message
        
    result["start"] = {
        "latitude": start_lat,
        "longitude": start_lng
    }
    
    result["end"] = {
        "latitude": end_lat,
        "longitude": end_lng
    }

    result["start_json"] = json.dumps(
        result["start"]
    )

    result["end_json"] = json.dumps(
        result["end"]
    )

    result["fuel_stops_json"] = json.dumps(
        result["fuel_stops"]
    )

    result["route_geometry_json"] = json.dumps(
        result["route_geometry"]
    )

    result["start_city"] = start_city or "New York"
    result["end_city"] = end_city or "Los Angeles"

    return render(
        request,
        "map.html",
        result
    )