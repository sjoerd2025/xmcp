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
   - Fill in the OAuth1 section (consumer key/secret and callback settings).
3. Run the server:
   - `python server.py`

The server starts at `http://127.0.0.1:8000` by default.
The MCP endpoint is `http://127.0.0.1:8000/mcp`.

## Environment variables

Required (OAuth1 user context):
- `TWITTER_CONSUMER_KEY`
- `TWITTER_CONSUMER_SECRET`
- `X_OAUTH_CALLBACK_HOST` (default `127.0.0.1`)
- `X_OAUTH_CALLBACK_PORT` (default `8976`)
- `X_OAUTH_CALLBACK_PATH` (default `/oauth/callback`)
- `X_OAUTH_CALLBACK_TIMEOUT` (default `300`)

Optional auth fallback:
- `X_BEARER_TOKEN` (OAuth2 bearer token)

Optional server config:
- `MCP_HOST` (default `127.0.0.1`)
- `MCP_PORT` (default `8000`)
- `X_API_BASE_URL` (default `https://api.x.com`)
- `X_API_TIMEOUT` (default `30`)
- `X_API_DEBUG` (default `1`)
- `FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER`

Tool filtering (comma-separated):
- `X_API_TOOL_TAGS`
- `X_API_TOOL_ALLOWLIST`
- `X_API_TOOL_DENYLIST`

Optional Grok test client:
- `XAI_API_KEY`
- `XAI_MODEL` (default `grok-4-1-fast`)
- `MCP_SERVER_URL` (default `http://127.0.0.1:8000/mcp`)

## Auth flow (OAuth1 on startup)

The server runs an OAuth1 browser flow on startup and uses the resulting
access token to sign every request. You must register a callback URL in your
X Developer App that matches:

```
http://<X_OAUTH_CALLBACK_HOST>:<X_OAUTH_CALLBACK_PORT><X_OAUTH_CALLBACK_PATH>
```

Example:

```
http://127.0.0.1:8976/oauth/callback
```

When you start the server, it will open a browser tab for consent and wait
for the callback. Tokens are kept in memory only for the lifetime of the
server process.

## Tool whitelisting

If you want to limit the tool list (smaller context window, fewer tools),
use `X_API_TOOL_ALLOWLIST` or `X_API_TOOL_TAGS` in `.env`.

Example allowlist:

```
X_API_TOOL_ALLOWLIST=getUsersByUsername,createDirectMessagesByParticipantId
```

Example tags:

```
X_API_TOOL_TAGS=users,dm
```

Allowlist and tags are applied at startup when the OpenAPI spec is loaded.

## Generate an OAuth2 user token (optional)

If you want a user-context OAuth2 token:
1. Add `CLIENT_ID` and `CLIENT_SECRET` to your `.env`.
2. Update `redirect_uri` in `generate_authtoken.py` to match your app settings.
3. Run `python generate_authtoken.py` and follow the prompts.
4. Copy the printed access token into `.env` as `X_OAUTH_ACCESS_TOKEN`.

## Run the Grok MCP test client (optional)

1. Set `XAI_API_KEY` in `.env`.
2. Make sure your MCP server is running locally (or set `MCP_SERVER_URL`).
3. If Grok cannot reach `http://127.0.0.1:8000/mcp`, use ngrok to tunnel your
   local server and point `MCP_SERVER_URL` to the public ngrok URL.
4. Run `python test_grok_mcp.py`.

## Notes

- Endpoints with `/stream` or `/webhooks` in the path are excluded.
- Operations tagged `Stream` or `Webhooks`, or marked with
  `x-twitter-streaming: true`, are excluded.
- The OpenAPI spec is fetched from `https://api.twitter.com/2/openapi.json` at
  startup.
