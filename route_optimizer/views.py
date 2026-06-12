from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
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

    start_lat = float(
        request.GET.get(
            "start_lat",
            40.7128
        )
    )

    start_lng = float(
        request.GET.get(
            "start_lng",
            -74.0060
        )
    )

    end_lat = float(
        request.GET.get(
            "end_lat",
            34.0522
        )
    )

    end_lng = float(
        request.GET.get(
            "end_lng",
            -118.2437
        )
    )

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

    return render(
        request,
        "map.html",
        result
    )