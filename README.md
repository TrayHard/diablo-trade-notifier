# Diablo Trade Notifier

[Русскоязычное README]

This app allows you to get notifications about any new messages on the website for trading with in-game items and 
services in Diablo 4 - https://diablo.trade/. I made it for myself and now sharing it with others. For now it works only
with telegram, but Discord or any other method with API - can be attached as well. 

To use it you will have to install Python, create your Telegram bot, keep your PC turned on and around 1-2 times a day
relaunch the app, changing the auth data, grabbing it manually from the browser (I'll show you how).

_A little disclaimer: I am not very familiar with Python, usually I work with JS, Python here been chosen only for interest and learning purposes,
so any recommendations in [Issues](https://github.com/TrayHard/diablo-trade-notifier/issues)
and [Pull Requests](https://github.com/TrayHard/diablo-trade-notifier/pulls) are welcome._

### Telegram:

![Screenshot](https://i.imgur.com/d6mRbvj.png)

### Usage:
- Install [Python 3](https://www.python.org/downloads/). 
- Clone the repo
- Install requirements: `pip install asyncio websockets requests python-dotenv`
- Create `.env` file and fill it up relying on `.env.example`
- Create "tokens.txt" file in the folder or just launch the app once, it will be created automatically.
- You need to put your auth data in "tokens.txt", to do that follow instructions in "**Authorizing**" section
- Launch the app. You should see something like this:
![Screenshot](https://i.imgur.com/4bSaT1u.png)
- Just leave it working, don't close it and you'll get notification once any new message will arrive on the website.
- 1-2 times a day you'll get an error message in telegram that your token expired:

![Screenshot](https://i.imgur.com/1UrIn0P.png)
- To fix this just repeat the actions from **Authorizing** section


#### .env file
Firstly you need to create your own Telegram bot and put its secret token in .env file to allow the app operate using your bot. 
To do that just follow official tg instructions, they are pretty simple - https://core.telegram.org/bots/tutorial.

Then you need to get your telegram ID. To do that just use [@userinfobot](https://t.me/userinfobot), and put Id from there
to `"RECIPIENT_TG_ID"` environment variable in `.env` file

#### Authorizing
1. Open diablo.trade and authorize yourself
2. Open dev tools in your browser (Ctrl + Shift + I in Chrome)
3. Open Network tab there. Select "WS" filter and click on the "websocket" line:

![Screenshot](https://i.imgur.com/0ryT8wO.png)
4. Then copy these 2 lines that are shown on screenshot - just right-click and select "Copy message":

![Screenshot](https://i.imgur.com/gb1alTr.png)
 
5. Paste it one by one (order is very important) into `tokens.txt` file and launch the app. In case there will be only 
one message - just copy and paste it as it is, just ensure that you have 2 lines in `tokens.txt`.
