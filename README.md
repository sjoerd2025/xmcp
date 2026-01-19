# X API FastMCP Server

This project exposes the X API OpenAPI spec as MCP tools using FastMCP, while
excluding streaming and webhook endpoints.

## Setup

1. Create a virtual environment and install dependencies:
   - `python -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`

2. Configure environment variables (example file at `env.example`):
   - `X_OAUTH_ACCESS_TOKEN` (preferred if set)
   - `X_BEARER_TOKEN` (fallback)
   - Optional: `X_API_BASE_URL`, `X_API_TIMEOUT`, `MCP_HOST`, `MCP_PORT`
   - Optional: `FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER`

3. Run the server:
   - `python server.py`

The server will start on `http://127.0.0.1:8000` by default.

## Notes

- Endpoints with `/stream` or `/webhooks` in the path are excluded.
- Operations tagged `Stream` or `Webhooks`, or marked with
  `x-twitter-streaming: true`, are excluded.
- OAuth2 user tokens are used when `X_OAUTH_ACCESS_TOKEN` is set; otherwise the
  bearer token is used.
