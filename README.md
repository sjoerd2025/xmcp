# X API FastMCP Server

Run a local MCP server that exposes the X API OpenAPI spec as tools using
FastMCP. Streaming and webhook endpoints are excluded.

## Prerequisites

- Python 3.9+
- An X Developer Platform app (to get tokens)
- Optional: an xAI API key if you want to run the Grok test client

## Quick start (local server)

1. Create a virtual environment and install dependencies:
   - `python -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`
2. Create your local `.env`:
   - `cp env.example .env`
   - Set `X_OAUTH_ACCESS_TOKEN` or `X_BEARER_TOKEN`
3. Run the server:
   - `python server.py`

The server starts at `http://127.0.0.1:8000` by default.
The MCP endpoint is `http://127.0.0.1:8000/mcp`.

## Environment variables

Required (set one):
- `X_OAUTH_ACCESS_TOKEN` (preferred; user context)
- `X_BEARER_TOKEN` (fallback)

Optional server config:
- `MCP_HOST` (default `127.0.0.1`)
- `MCP_PORT` (default `8000`)
- `X_API_BASE_URL` (default `https://api.x.com`)
- `X_API_TIMEOUT` (default `30`)
- `X_API_DEBUG` (default `1`)
- `FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER`

Optional tool filtering (comma-separated):
- `X_API_TOOL_TAGS`
- `X_API_TOOL_ALLOWLIST`
- `X_API_TOOL_DENYLIST`

Optional Grok test client:
- `XAI_API_KEY`
- `XAI_MODEL` (default `grok-4-1-fast`)
- `MCP_SERVER_URL` (default `http://127.0.0.1:8000/mcp`)

## Generate an OAuth user token (optional)

If you want a user-context token:
1. Add `CLIENT_ID` and `CLIENT_SECRET` to your `.env`.
2. Update `redirect_uri` in `generate_authtoken.py` to match your app settings.
3. Run `python generate_authtoken.py` and follow the prompts.
4. Copy the printed access token into `.env` as `X_OAUTH_ACCESS_TOKEN`.

## Run the Grok MCP test client (optional)

1. Set `XAI_API_KEY` in `.env`.
2. Make sure your MCP server is running locally (or set `MCP_SERVER_URL`).
3. Run `python test_grok_mcp.py`.

## Notes

- Endpoints with `/stream` or `/webhooks` in the path are excluded.
- Operations tagged `Stream` or `Webhooks`, or marked with
  `x-twitter-streaming: true`, are excluded.
- OAuth2 user tokens are used when `X_OAUTH_ACCESS_TOKEN` is set; otherwise the
  bearer token is used.
