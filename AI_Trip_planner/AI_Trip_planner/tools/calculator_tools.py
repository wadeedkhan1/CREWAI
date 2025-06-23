from crewai.tools import tool

@tool("Make a Calculator")
def calculate(operation: str) -> str:
    """Evaluate a basic math expression like 2+2 or 10/5."""
    try:
        return str(eval(operation))
    except:
        return "Error: Invalid operation"