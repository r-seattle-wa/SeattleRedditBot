The gist:

All you should need is a `bot.py` config file that looks like this:

```
# Discord API Token
DISCORD_TOKEN=''
# Reddit API bot client ID
REDDIT_CLIENT_ID=''
# Reddit API bot client secret 
REDDIT_CLIENT_SECRET=''
# Reddit password
REDDIT_PASSWORD=''
# Sub to post to (no r/ needed)
REDDIT_SUB=''
# Reddit Username (Typically the bot)
REDDIT_USERNAME=''
# A user agent information for the reddit API (e.g. 'A praw based bot for r/SeattleWA')
REDDIT_USER_AGENT=''
# For markov sampling
STATE_SIZE=
```

STATE_SIZE is recommended to be set to 2