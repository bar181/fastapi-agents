# master/app/main.py
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse, Response
from app.routes.routes_llm import router as llm_router
from app.routes.routes_simple import router as simple_router
# from app.routes.routes_dynamic import router as dynamic_router
# from app.routes.routes_validation import router as validation_router
# from app.routes.routes_miprov2_core import router as miprov2_core_router
# from app.routes.routes_classification import router as classification_router  # REMOVED
from app.routes.routes_dspy import router as dspy_router 

app = FastAPI(title="Agent Framework - Master Module")

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "ok", "message": "Healthy"})

@app.get("/favicon.ico")
async def get_favicon():
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
        <rect width="16" height="16" fill="#4a90e2"/>
        <text x="2" y="12" font-size="10" fill="white">A</text>
    </svg>'''
    return Response(content=svg.encode('utf-8'), media_type="image/svg+xml")

# Include routers
app.include_router(llm_router, prefix="/llm")
app.include_router(simple_router, prefix="/simple")
# app.include_router(dynamic_router, prefix="/dynamic")
# app.include_router(validation_router, prefix="/validation")
# app.include_router(miprov2_core_router, prefix="/miprov2")
# app.include_router(classification_router, prefix="/classification")  # REMOVED
app.include_router(dspy_router, prefix="/dspy")