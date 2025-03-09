# master/app/routes/routes_simple.py
from fastapi import APIRouter
from agents.simple.hello_world import register_routes as register_hello_world_routes
from agents.simple.time import register_routes as register_time_routes
from agents.simple.quote import register_routes as register_quote_routes

router = APIRouter()

register_hello_world_routes(router)  # Corrected: Call the functions
register_time_routes(router)        # Corrected: Call the functions
register_quote_routes(router)       # Corrected: Call the functions