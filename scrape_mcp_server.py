from typing import Any, Dict, Optional, List
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("scrape-service")

# Constants
API_ENDPOINT = "http://localhost:8000/api/v1/scrape"
TIMEOUT = 30  # seconds

async def make_scrape_request(params: Dict[str, Any]) -> Dict[str, Any]:
    """Make a request to the scrape API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                API_ENDPOINT, 
                json=params,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

@mcp.tool()
async def scrape_url(
    url: str, 
    get_full_content: bool = True,
    only_main_content: bool = True
) -> str:
    """Scrape content from a URL and return the content.
    
    Args:
        url: The URL to scrape
        get_full_content: Whether to get full content or just metadata
        only_main_content: Whether to extract only the main content
    """
    # Configure parameters
    params = {
        "url": url,
        "formats": ["markdown", "html"],
        "onlyMainContent": only_main_content,
        "includeRawHtml": False,
        "includeScreenshot": False
    }
    
    # Make the API call
    result = await make_scrape_request(params)
    
    if not result.get("success", False):
        error_msg = result.get("error", "Unknown error")
        return f"Error scraping {url}: {error_msg}"
    
    data = result.get("data", {})
    metadata = data.get("metadata", {})
    title = metadata.get("title", "No title")
    description = metadata.get("description", "")
    
    # If only metadata is requested
    if not get_full_content:
        # Format links for display
        links = data.get("links", [])
        formatted_links = '\n'.join([f"- {link}" for link in links[:5]])
        if len(links) > 5:
            formatted_links += f"\n... and {len(links) - 5} more links"
            
        return f"""
# {title}

{description}

## Links
{formatted_links if links else "No links found."}
        """.strip()
    
    # Return full content
    markdown_content = data.get("markdown", "No content available")
    return f"""
# {title}

{description}

## Content

{markdown_content}
    """.strip()

@mcp.tool()
async def scrape_advanced(
    url: str,
    mobile: bool = False,
    include_raw_html: bool = False,
    wait_time: Optional[int] = None,
    custom_headers: Optional[Dict[str, str]] = None
) -> str:
    """Advanced web scraping with additional options.
    
    Args:
        url: The URL to scrape
        mobile: Whether to use mobile user agent
        include_raw_html: Whether to include raw HTML in response
        wait_time: Time to wait after page load in milliseconds
        custom_headers: Custom HTTP headers to send with request
    """
    # Configure parameters
    params = {
        "url": url,
        "formats": ["markdown", "html"],
        "onlyMainContent": True,
        "includeRawHtml": include_raw_html,
        "mobile": mobile
    }
    
    if wait_time is not None:
        params["waitFor"] = wait_time
        
    if custom_headers is not None:
        params["headers"] = custom_headers
    
    # Make the API call
    result = await make_scrape_request(params)
    
    if not result.get("success", False):
        error_msg = result.get("error", "Unknown error")
        return f"Error scraping {url}: {error_msg}"
    
    data = result.get("data", {})
    metadata = data.get("metadata", {})
    title = metadata.get("title", "No title")
    description = metadata.get("description", "")
    markdown_content = data.get("markdown", "No content available")
    
    return f"""
# {title}

{description}

## Content

{markdown_content}
    """.strip()

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')