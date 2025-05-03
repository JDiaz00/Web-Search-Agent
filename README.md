# Multi-Agent System

A multi-agent system built with LangChain that uses specialized agents for different tasks.

## Features

- Specialized agents for different tools
- Router agent for directing queries to the appropriate specialized agent
- Environment variable support for API keys

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry for dependency management

### Installation

1. Clone the repository
2. Install dependencies using Poetry:
   ```
   poetry install
   ```

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# API Keys
SERPAPI_KEY="your-serpapi-key-here"

# Add other environment variables as needed
```

## Available Agents

- **Calculator Agent**: Handles mathematical calculations and expressions
- **Cinema Agent**: Searches for cinemas in specific locations using SerpAPI

## Usage

Start the API server:

```
poetry run python src/main.py
```

Then make requests to the API with your queries. 