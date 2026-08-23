from fastmcp import FastMCP

mcp = FastMCP(name="My FastM")

@mcp.tool()
def add(a: int, b: int):
    '''Add two numbers together.'''
    return a + b

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)