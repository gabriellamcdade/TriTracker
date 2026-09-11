import json
import os
import secrets
import threading
import time
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


def load_tokens():
    try:
        with open(TOKEN_FILE, "r") as file:
            tokens = json.load(file)

    except FileNotFoundError:
        raise RuntimeError(
            "No saved Strava tokens were found. "
            "Connect TriTracker to Strava first."
        )

    except json.JSONDecodeError:
        raise RuntimeError(
            "The saved Strava token file is not valid JSON."
        )

    if "access_token" not in tokens:
        raise RuntimeError(
            "The saved Strava token file does not "
            "contain an access token."
        )

    return tokens


def exchange_code_for_tokens(code):
    try:
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

    except requests.RequestException as error:
        raise RuntimeError(
            f"Could not exchange the Strava code: {error}"
        )

    try:
        tokens = response.json()

    except ValueError:
        raise RuntimeError(
            "Strava returned invalid token data."
        )

    save_tokens(tokens)

    return tokens


def refresh_access_token(refresh_token):
    try:
        response = requests.post(
            "https://www.strava.com/api/v3/oauth/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            timeout=20,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise RuntimeError(
            f"Could not refresh the Strava token: {error}"
        )

    try:
        tokens = response.json()

    except ValueError:
        raise RuntimeError(
            "Strava returned invalid token data."
        )

    save_tokens(tokens)

    return tokens


def get_valid_tokens():
    tokens = load_tokens()

    expires_at = tokens.get("expires_at", 0)

    # Refresh slightly before expiry so a token does not
    # expire in the middle of a request.
    if expires_at <= int(time.time()) + 60:
        refresh_token = tokens.get("refresh_token")

        if not refresh_token:
            raise RuntimeError(
                "No Strava refresh token was found. "
                "Reconnect TriTracker to Strava."
            )

        tokens = refresh_access_token(
            refresh_token
        )

    return tokens


def connect_to_strava():
    if not CLIENT_ID:
        raise RuntimeError(
            "STRAVA_CLIENT_ID is missing from .env."
        )

    if not CLIENT_SECRET:
        raise RuntimeError(
            "STRAVA_CLIENT_SECRET is missing from .env."
        )

    if not REDIRECT_URI:
        raise RuntimeError(
            "STRAVA_REDIRECT_URI is missing from .env."
        )

    parsed_redirect = urlparse(REDIRECT_URI)

    callback_host = (
        parsed_redirect.hostname or "localhost"
    )

    callback_port = parsed_redirect.port

    if callback_port is None:
        raise RuntimeError(
            "STRAVA_REDIRECT_URI must include a port."
        )

    state = secrets.token_urlsafe(16)
    callback_result = {}

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            query = parse_qs(
                urlparse(self.path).query
            )

            returned_state = query.get(
                "state",
                [None],
            )[0]

            if returned_state != state:
                self.send_response(400)
                self.end_headers()

                self.wfile.write(
                    b"Invalid OAuth state."
                )

                return

            if "error" in query:
                callback_result["error"] = (
                    query["error"][0]
                )

            elif "code" in query:
                callback_result["code"] = (
                    query["code"][0]
                )

                callback_result["scope"] = (
                    query.get(
                        "scope",
                        [""],
                    )[0]
                )

            self.send_response(200)
            self.end_headers()

            self.wfile.write(
                b"Strava connected successfully. "
                b"You can close this tab."
            )

        def log_message(self, format, *args):
            return

    try:
        server = HTTPServer(
            (
                callback_host,
                callback_port,
            ),
            CallbackHandler,
        )

    except OSError as error:
        raise RuntimeError(
            f"Could not start the Strava callback "
            f"server on port {callback_port}: {error}"
        )

    server_thread = threading.Thread(
        target=server.handle_request,
        daemon=True,
    )

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
            "Strava authorization was not granted: "
            f"{callback_result['error']}"
        )

    if "code" not in callback_result:
        raise RuntimeError(
            "Strava did not return an authorization code."
        )

    if (
        "activity:read_all"
        not in callback_result.get("scope", "")
    ):
        raise RuntimeError(
            "TriTracker needs activity:read_all permission."
        )

    return exchange_code_for_tokens(
        callback_result["code"]
    )


def authenticated_get(url, params=None):
    tokens = get_valid_tokens()

    headers = {
        "Authorization": (
            f"Bearer {tokens['access_token']}"
        )
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20,
        )

    except requests.Timeout:
        raise RuntimeError(
            "The request to Strava timed out. "
            "Please try again."
        )

    except requests.RequestException as error:
        raise RuntimeError(
            f"Could not connect to Strava: {error}"
        )

    # If Strava rejects the token unexpectedly,
    # refresh once and retry.
    if response.status_code == 401:
        refresh_token = tokens.get(
            "refresh_token"
        )

        if not refresh_token:
            raise RuntimeError(
                "Your Strava session has expired "
                "and cannot be refreshed."
            )

        tokens = refresh_access_token(
            refresh_token
        )

        headers = {
            "Authorization": (
                f"Bearer {tokens['access_token']}"
            )
        }

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=20,
            )

        except requests.RequestException as error:
            raise RuntimeError(
                f"Could not connect to Strava: {error}"
            )

    try:
        response.raise_for_status()

    except requests.HTTPError:
        raise RuntimeError(
            "Strava returned an error: "
            f"{response.status_code}"
        )

    try:
        return response.json()

    except ValueError:
        raise RuntimeError(
            "Strava returned a response "
            "that was not valid JSON."
        )


def get_authenticated_athlete():
    return authenticated_get(
        "https://www.strava.com/api/v3/athlete"
    )


def get_activities(page=1, per_page=10):
    if page < 1:
        raise ValueError(
            "page must be 1 or greater."
        )

    if not 1 <= per_page <= 200:
        raise ValueError(
            "per_page must be between 1 and 200."
        )

    return authenticated_get(
        "https://www.strava.com/api/v3/"
        "athlete/activities",
        params={
            "page": page,
            "per_page": per_page,
        },
    )