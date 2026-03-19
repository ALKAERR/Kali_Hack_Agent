"""Tools for container execution."""

from agents import function_tool
from core.docker_executor import KaliDockerExecutor
from dotenv import load_dotenv
import os

load_dotenv()
docker_exec = KaliDockerExecutor(os.environ.get('DOCKER_NAME'))

@function_tool
def python_execute(code: str, rationale: str = "") -> str:
    """Execute Python code in Kali Linux Docker container.
    
    Args:
        code: Python code to execute
        rationale: Optional explanation for why this code is being executed
        
    Returns:
        Execution result as string
    """
    return docker_exec.execute(code)

