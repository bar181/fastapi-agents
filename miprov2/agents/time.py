# agents/time.py
from typing import Dict, Any
from fastapi import APIRouter
from datetime import datetime, UTC 

class TimeAgent:
    """
    Time Agent
    -----------
    Purpose: Returns the current time in ISO 8601 format.
    """
    
    def get_time(self) -> Dict[str, str]:
        """Returns the current time in ISO 8601 format."""
        current_time = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        return {"time": current_time}
    
# Keep the original function for backward compatibility
def agent_main():
    """
    Original agent_main function for backward compatibility.
    """
    agent = TimeAgent()
    return agent.get_time()

def register_routes(router: APIRouter):
    """Registers the time agent's routes with the provided APIRouter."""
    
    agent = TimeAgent()
    
    @router.get("/time", summary="Returns the current time in ISO 8601 format.", tags=["Simple Agents"])
    async def time_route():
        """
        Returns the current time in ISO 8601 format.
        
        **Process:** An instance of the `TimeAgent` is used to generate the response.
        
        **Example Output:**
        
        ```json
        {
          "agent": "time",
          "result": {
            "time": "2025-02-23T20:00:00Z"
          }
        }
        ```
        """
        return {"agent": "time", "result": agent.get_time()}