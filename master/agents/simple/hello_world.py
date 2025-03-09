# master/agents/simple/hello_world.py
from fastapi import APIRouter

# NO router = APIRouter() here

def register_routes(router: APIRouter):
    @router.get("/hello_world", tags=["Simple Agents"])
    async def read_hello_world():
        """
        Returns a simple hello world message.
        """
        return {"message": "Hello World"}