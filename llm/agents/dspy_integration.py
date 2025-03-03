import importlib.util
import os

def load_agent(agent_filename: str):
    """Dynamically load an agent module from a given filename."""
    module_name = os.path.splitext(os.path.basename(agent_filename))[0]
    spec = importlib.util.spec_from_file_location(module_name, agent_filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_agent(agent_module):
    """Run the agent's main function (agent_main) and return its output."""
    if hasattr(agent_module, "agent_main"):
        return agent_module.agent_main()
    else:
        raise AttributeError("The agent does not define 'agent_main'.")