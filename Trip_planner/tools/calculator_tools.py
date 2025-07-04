from crewai.tools import tool

@tool("Calculator")
def calculate(expression: str) -> str:
    """Calculates the result of a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}" 