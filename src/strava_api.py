import json
import os
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI")

TOKEN_FILE = "data/strava_tokens.json"


def save_tokens(tokens):
    with open(TOKEN_FILE, "w") as file:
        json.dump(tokens, file, indent=2)


def exchange_code_for_tokens(code):
    response = requests.post(
        "https://www.strava.com/api/v3/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
        },
        timeout=20,
    )

    response.raise_for_status()
    tokens = response.json()

    save_tokens(tokens)
    return tokens


def connect_to_strava():
    state = secrets.token_urlsafe(16)
    callback_result = {}

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            query = parse_qs(urlparse(self.path).query)

            if query.get("state", [None])[0] != state:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid OAuth state.")
                return

            if "error" in query:
                callback_result["error"] = query["error"][0]
            else:
                callback_result["code"] = query["code"][0]
                callback_result["scope"] = query.get("scope", [""])[0]

            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                b"Strava connected successfully. You can close this tab."
            )

        def log_message(self, format, *args):
            return

    server = HTTPServer(("localhost", 8000), CallbackHandler)

    server_thread = threading.Thread(target=server.handle_request)
    server_thread.start()

    parameters = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "approval_prompt": "auto",
        "scope": "activity:read_all",
        "state": state,
    }

    authorization_url = (
        "https://www.strava.com/oauth/authorize?"
        + urlencode(parameters)
    )

    print("Opening Strava in your browser...")
    webbrowser.open(authorization_url)

    server_thread.join()
    server.server_close()

    if "error" in callback_result:
        raise RuntimeError(
            f"Strava authorization was not granted: "
            f"{callback_result['error']}"
        )

    if "activity:read_all" not in callback_result["scope"]:
        raise RuntimeError(
            "TriTracker needs activity:read_all permission."
        )

    return exchange_code_for_tokens(callback_result["code"])