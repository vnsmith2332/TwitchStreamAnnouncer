# TwitchStreamAnnouncer
A bot that announces new Twitch streams to Reddit

## Prerequisites
Below are the requirements to run this bot on your personal computer:
1. The Python programming language installed on your computer. [Download it here.](https://www.python.org/downloads/)
2. A Reddit account
3. A Twitch account
4. Basic understanding of how to use Powershell (Windows) or the terminal (MacOS/Linux).

## Setup
Some simple setup is required to use the TwitchStreamAnnouncer.

### Register an application with Reddit
You must register an application with Reddit in order to obtain the requisite credentials to use a bot. Follow the steps under the section "First Steps" on [this page](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) to register your Reddit application. Make note of the client ID and client secret for your app; you will need them later.

### Register an application with Twitch
You must register an application with Reddit in order to obtain the requisite credentials to use a bot. Follow the steps on this page to register your Twitch application. Make note of the client ID and secret for your app; you will need them later. 

**WARNING:** Twitch does not allow you to view your application's secret after it is generated. Save it now or you will have to generate a new one later.

### Install required packages (Windows)
There are some Python packages that need to be installed on your computer to run the bot. Open Powershell and run the following commands, one at a time:
```shell
py -3 -m pip install praw
py -3 -m pip install requests
```

### Install required packages (MacOS/Linux)
There are some Python packages that need to be installed on your computer to run the bot. Open the terminal and run the following commands, one at a time:
```shell
pip3 install praw
pip3 install requests
```

### Download and edit the code
You will need to make some simple code changes. Download [main.py](https://github.com/vnsmith2332/TwitchStreamAnnouncer/blob/main/main.py) from this repository. Open the file in a text editor. This can be an IDE or your computer's built-in text editor. Near the top of this file, there are several lines of code that you need to change:

* `TWITCH_CLIENT_ID = "YOUR TWITCH CLIENT ID"`: Change the text inside the quotation marks to the client ID you obtained when registering your Twitch application.
* `TWITCH_CLIENT_SECRET = "YOUR TWITCH CLIENT SECRET"`: Change the text inside the quotation marks to the secret you obtained when registering your Twitch application.
* `TWITCH_USER_NAME = "YOUR TWITCH USERNAME"`: Change the text inside the quoatation marks to the username of the Twitch streamer you would like to monitor.

* `REDDIT_CLIENT_ID = "YOUR REDDIT CLIENT ID"`: Change the text inside the quotation marks to the client ID you obtained when registering your Reddit application.
* `REDDIT_CLIENT_SECRET = "YOUR REDDIT CLIENT SECRET"`: Change the text inside the quotation marks to the client secret you obtained when registering your Reddit application.
* `REDDIT_USER_AGENT = "<YOUR REDDIT APPLICATION NAME>"`: Change the text inside the angled brackets to the name of your Reddit application.
* `REDDIT_USER_NAME = "YOUR REDDIT USERNAME"`: Change the text inside the quotation marks to your Reddit account username.
* `REDDIT_PASSWORD = "YOUR REDDIT PASSWORD"`: Change the text inside the quotation marks to your Reddit account password.
* `SUBREDDIT = "YOUR SUBREDDIT"`: Change the text inside the quotation marks to the name of the subreddit you would like to announce new Twitch streams in (ex: if you would like to announce your streams in r/test, you would set change the text to "test").

* `FREQUENCY = 300`: Change this number to the amount of time, *in seconds*, you would like to wait between checking for a new Twitch stream.

Save your changes and close the file.

## Running the Bot (Windows)
Now that your setup is complete, you are ready to run the bot! Open Powershell and run the following commands, one at a time. **Replace the text "C:/Path/To/.py/File" with the path to the code file you downloaded during setup**:
```shell
cd C:/Path/To/.py/File
python3 main.py
```
Now the bot should be running!

## Running the Bot (MacOS/Linux)
Now that your setup is complete, you are ready to run the bot! Open Powershell and run the following commands, one at a time. **Replace the text "/Path/To/.py/File" with the path to the code file you downloaded during setup**:
```shell
cd /Path/To/.py/File
python3 main.py
```
Now the bot should be running!

## Customization
You can customize the Reddit post the TwitchStreamAnnouncer makes with some simple code changes:
* To customize the title, find `title = f"{TWITCH_USER_NAME} is now streaming live on Twitch!!!"` within the function `announce_stream` (line 122). Change the text in quotation marks to your desired title.
* To customize the body of the post, find `content = f"Watch me play {stream['data'][0]['game_name']} at https://www.twitch.tv/{TWITCH_USER_NAME}"` within the function `announce_stream` (line 123). Change the text in quotation marks to your desired title.

## Troubleshooting
There is a chance you will encounter problems while using this bot. Common problems you may face - and how to fix them - follow:
* `cd: no such file or directory`: This error may occur when trying to navigate to the bot file using the `cd` command in the terminal/Powershell. If this error occurs, you have entered the path to the bot file incorrectly. Check the file's path and try again. For more information on file paths, read [this article.](https://www.codecademy.com/resources/docs/general/file-paths)
* `FileNotFoundError`: This error may occur when trying to run the bot with the command `python3 main.py`. It means Python was not able to locate the file you program you tried to execute. If this error occurs, ensure you used the `cd` command to enter the directory containing the bot file and try again.
* `CredentialError`: This error occurs if your Twitch and/or Reddit credentials are invalid. This error is usually accompanied by a helpful message. Read this message to help identify the problem. Regardless of the message, the problem will pertain to the credentials you configured as a part of this guide. Ensure these credentials are correct.
