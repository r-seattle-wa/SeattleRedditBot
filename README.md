## Seattle Reddit Bot [![pipeline status](https://gitlab.com/seattlewa/SeattleRedditBot/badges/master/pipeline.svg)](https://gitlab.com/seattlewa/SeattleRedditBot/commits/master)
---

#### daily_post.py
###### Creates daily reddit post that includes:
- ###### A list of event calendars
- ###### An emoji-fied 2-day weather forecast
- ###### A quote of the day
- ###### A link to our discord server
- ###### A link to our archives
###### Template used: `templates/daily_post.j2`
---

### Configuration
##### Create a `bot.py` config file in the base dir with the following properties:  

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
# For markov sampling (recommended to be 2)
STATE_SIZE=
```
