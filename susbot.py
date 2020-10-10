import sys
import irc.bot
import requests
import praw
import os
import time

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
        

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        if e.arguments[0].startswith('!commands edit !sus ') and e.source.nick == 'jerma985':
            sus = str(e.arguments[0]).split('!commands edit !sus ', 1)[1]
            print('New sus: ' + sus)
            print(e.source.nick)
            reddit = login_reddit()
            reddit.validate_on_submit = True
            if len(sus) > 300:
                susTruncated = sus[:297]
                susPost = sus[297:]
                while True:
                    try:
                        reddit.subreddit("jerma985").submit(susTruncated + "...", selftext="..." + susPost + " JermaSusBot by /u/Thestickman391")
                        print("Posted to reddit!")
                        break
                    except praw.exceptions.RedditAPIException as exception:
                        totalLength = str(exception.items[0].message).split('you are doing that too much. try again in ', 1)[1]
                        minutesToSleep = totalLength[0].partition("minutes.")[0]
                        secondsToSleep = int(minutesToSleep) * 60
                        print("Sleeping for " + str(secondsToSleep) + " seconds")
                        time.sleep(secondsToSleep)
            else:
                while True:
                    try:
                        reddit.subreddit("jerma985").submit(sus, selftext="JermaSusBot by /u/Thestickman391")
                        print("Posted to reddit!")
                        break
                    except praw.exceptions.RedditAPIException as exception:
                        totalLength = str(exception.items[0].message).split('you are doing that too much. try again in ', 1)[1]
                        minutesToSleep = totalLength[0].partition("minutes.")[0]
                        secondsToSleep = int(minutesToSleep) * 60
                        print("Sleeping for " + str(secondsToSleep) + " seconds")
                        time.sleep(secondsToSleep)
                
def main():
    username  = "Thestickman391"
    client_id = "foo"
    token     = "bar"
    channel   = "jerma985"

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()

def login_reddit():
    reddit = praw.Reddit(username = "JermaSusBot",
             password = "foo",
             client_id = "bar",
             client_secret = "foo",
             user_agent = "JermaSusBot by /u/Thestickman301")
    print("Successfully logged into Reddit!")
    return reddit

if __name__ == "__main__":
    main()
