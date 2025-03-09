# master/app/routes/routes_dspy.py
from fastapi import APIRouter
from agents.dspy.dspy_classifier import register_routes as register_dspy_classifier

router = APIRouter()

# Register routes for DSPy agents
register_dspy_classifier(router)