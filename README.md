# Claude Web Scraper MCP

A simple Model Context Protocol (MCP) server that connects Claude for Desktop to a locally running eGet web scraper. This allows Claude to scrape website content through your local API.

## Prerequisites

- Claude for Desktop
- Python 3.7+
- eGet web scraper (from https://github.com/vishwajeetdabholkar/eGet-Crawler-for-ai)

## Setup Instructions

### 1. Set up eGet Web Scraper

First, make sure you have the eGet web scraper running:

```bash
# Clone the eGet repository
git clone https://github.com/vishwajeetdabholkar/eGet-Crawler-for-ai
cd eGet-Crawler-for-ai

# Set up and run eGet according to its instructions
# (typically using Docker or local Python installation)

# Verify the API is running (default: http://localhost:8000/api/v1/scrape)
```

### 2. Set up the MCP Server

```bash
# Create project directory
mkdir claude-scraper-mcp
cd claude-scraper-mcp

# Set up UV and virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv add "mcp[cli]" httpx

# Create the MCP server script
touch scrape_mcp_server.py
```

Copy the `scrape_mcp_server.py` code into the file.

### 3. Configure Claude for Desktop

1. Create or edit the Claude desktop configuration:

```bash
# On macOS
mkdir -p ~/Library/Application\ Support/Claude/
```

2. Add this configuration to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "scrape-service": {
            "command": "/absolute/path/to/claude-scraper-mcp/.venv/bin/python",
            "args": [
                "/absolute/path/to/claude-scraper-mcp/scrape_mcp_server.py"
            ]
        }
    }
}
```

Replace the paths with the actual absolute paths to your virtual environment and script.

3. Restart Claude for Desktop

## Usage

Once set up, you can use Claude to scrape websites with commands like:

- "Scrape the content from https://example.com and summarize it"
- "Get information about the website at https://news.ycombinator.com"

## Troubleshooting

If you encounter issues:

1. Check that eGet scraper is running
2. Verify the API endpoint in the script matches your eGet configuration
3. Make sure Claude for Desktop is using the correct Python interpreter
4. Restart Claude for Desktop after making changes to the configuration