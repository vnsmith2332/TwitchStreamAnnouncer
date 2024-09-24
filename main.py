import requests
import praw
from prawcore.exceptions import OAuthException, ResponseException
import time

# twitch auth details
TWITCH_CLIENT_ID = "YOUR TWITCH CLIENT ID"
TWITCH_CLIENT_SECRET = "YOUR TWITCH CLIENT SECRET"
TWITCH_USER_NAME = "YOUR TWITCH USERNAME"

# reddit auth details
REDDIT_CLIENT_ID = "YOUR REDDIT CLIENT ID"
REDDIT_CLIENT_SECRET = "YOUR REDDIT CLIENT SECRET"
REDDIT_USER_AGENT = "<TwitchStreamAnnouncer 1.0>"
REDDIT_USER_NAME = "YOUR REDDIT USERNAME"
REDDIT_PASSWORD = "YOUR REDDIT PASSWORD"
SUBREDDIT = "YOUR SUBREDDIT"

# Frequency to check if currently streaming on twitch (in seconds)
FREQUENCY = 300


class CredentialError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_client_credentials() -> dict:
    """
    Retrieve the client credentials necessary for an application to call the Twitch API
    :return:
    """
    client_credentials = requests.post(
        url="https://id.twitch.tv/oauth2/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "client_id": TWITCH_CLIENT_ID,
            "client_secret": TWITCH_CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
    )

    if client_credentials.status_code == 400:
        raise CredentialError(f"The Twitch client ID f{TWITCH_CLIENT_ID} is invalid. Correct it and try again.")
    if client_credentials.status_code == 403:
        raise CredentialError(f"The Twitch client secret f{TWITCH_CLIENT_SECRET} is invalid. Correct it and try again.")
        
    client_credentials = client_credentials.json()
    print(f"Obtained client credentials!\nBearer token: {client_credentials['access_token']}")
    return client_credentials


def is_streaming() -> bool:
    """
    Determine if a Twitch user is actively streaming
    :return:
    """
    streams = get_streams()
    return len(streams["data"]) > 0


def get_streams() -> dict:
    """
    Retrieve a Twitch user's active streams
    :return:
    """
    print("Getting active Twitch streams (if any)...")
    client_credentials = get_client_credentials()
    streams = requests.get(
        url=f"https://api.twitch.tv/helix/streams?user_login={TWITCH_USER_NAME}",
        headers={
            "Authorization": f"Bearer {client_credentials['access_token']}",
            "Client-Id": TWITCH_CLIENT_ID
        }
    )
    return streams.json()


def stream_is_new(stream: dict) -> bool:
    """
    Determine if the bot has seen the current stream before
    :param stream:
    :return:
    """
    old_streams = get_past_streams()
    return not stream["data"][0]["id"] in old_streams


def get_past_streams() -> set:
    """
    Read a file of old stream IDs maintained by the bot.
    :return:
    """
    try:
        with open("stream_ids.txt", "r") as f:
            return set([line.strip() for line in f.readlines()])
    except FileNotFoundError:
        return set()


def process_new_stream(stream: dict):
    record_stream(stream)
    announce_stream(stream)


def record_stream(stream: dict) -> None:
    """
    Add a new stream to the list of streams the bot has seen before.
    :param stream:
    :return:
    """
    with open("stream_ids.txt", "a+") as f:
        f.write(stream["data"][0]["id"] + "\n")
    print(f"Recorded stream {stream['data'][0]['id']} in stream_ids.txt.")


def announce_stream(stream: dict) -> None:
    """
    Post an announcement of a new stream
    :param stream:
    :return:
    """
    print(f"Announcing stream {stream['data'][0]['id']} to r/{SUBREDDIT}")

    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
            username=REDDIT_USER_NAME,
            password=REDDIT_PASSWORD
        )

        title = f"{TWITCH_USER_NAME} is now streaming live on Twitch!!!"
        content = f"Watch me play {stream['data'][0]['game_name']} at https://www.twitch.tv/{TWITCH_USER_NAME}"

        subreddit = reddit.subreddit(SUBREDDIT)
        subreddit.submit(
            title=title,
            selftext=content
        )
    except ResponseException:
        raise CredentialError("Invalid Reddit client ID and/or invalid Reddit client secret. Check these credentials and try again.")
    except OAuthException:
        raise CredentialError("Invalid Reddit username and/or invalid Reddit password. Check these credentials and try again.")

    print(f"Successfully announced the stream in r/{SUBREDDIT}!")


def bot() -> None:
    while True:
        if is_streaming():
            print(f"{TWITCH_USER_NAME} is streaming live! Checking if the stream is new...")
            stream = get_streams()
            if stream_is_new(stream):
                print(f"Stream {stream['data'][0]['id']} is a new stream! Announcing the stream to r/{SUBREDDIT}.")
                process_new_stream(stream)
            else:
                print(
                    f"Stream {stream['data'][0]['id']} has already been announced. Checking for a new stream in {FREQUENCY} seconds...")
        else:
            print(f"{TWITCH_USER_NAME} is not currently streaming. Checking again in {FREQUENCY} seconds...")
        print(f"{'-' * 100}\n\n")
        time.sleep(FREQUENCY)


if __name__ == "__main__":
    bot()
