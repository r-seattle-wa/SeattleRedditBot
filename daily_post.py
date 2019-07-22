#!/usr/bin/env python
from typing import Any, Dict, Optional
import datetime
import json
import re

from jinja2 import Environment, FileSystemLoader
import praw
import requests

from bot import *
import daily_markov


NWS_FORECAST_URL = 'https://api.weather.gov/gridpoints/SEW/123,68/forecast'
ASTRO_APP_MOON_API_URL = 'https://api.usno.navy.mil/moon/phase'


class Emojis:
    NewMoon = '\U0001F31A'
    FirstQuarterMoon = '\U0001F31B'
    ThirdQuarterMoon = '\U0001F31C'
    FullMoon = '\U0001F31D'
    Sun = '\U0001F31E'
    Cloud = '\u2601'
    SunBehindCloud = '\u26C5'
    RainAndLightning = '\u26C8'
    Rain = '\U0001F327'
    Snow = '\U0001F328'
    Lightning = '\U0001F329'
    Fog = '\U0001F301'
    NightWithStars = '\U0001F303'
    FearfulFace = '\U0001F628'


def _convert_time_str_to_datetime(time: str) -> datetime.datetime:
    time = re.sub(r'([-+]\d\d):(\d\d)', r'\1\2', time)
    return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')


def get_moon_phase(date: datetime.datetime) -> str:
    response = requests.get(ASTRO_APP_MOON_API_URL, params={
        'date': date.strftime('%m/%d/%Y'),
        'nump': 1
    })
    data = response.json()

    if data['error']:
        raise Exception('Moon phase API returned error: {}'
                        .format(data['type']))

    phase_name = data['phasedata'][0]['phase']
    if phase_name == 'New Moon':
        return Emojis.NewMoon
    elif phase_name == 'First Quarter':
        return Emojis.FirstQuarterMoon
    elif phase_name == 'Full Moon':
        return Emojis.FullMoon
    elif phase_name == 'Last Quarter':
        return Emojis.ThirdQuarterMoon
    else:
        raise Exception('Moon phase API returned an unexpected phase name: {}'
                        .format(phase_name))


def get_weather_emoji(period: Dict[str, Any]) -> Optional[str]:
    # only get the first phrase in the short forecast
    match = re.match(r'^((?:[A-Z]\w+ )*[A-Z]\w+)', period['shortForecast'])
    if match is None:
        return None

    night = not period['isDaytime']
    short_forecast = match.group(1).lower()

    rainy_regex = r'.*rain.*'
    cloudy_regex = r'(?:mostly )?cloudy'
    partly_cloudy_regex = r'partly (?:sunny|cloudy)'
    sunny_regex = r'(?:mostly )?sunny'
    thunderstorm_regex = r'.*showers and thunderstorms.*'
    clear_regex = r'(?:mostly )?clear'
    fog_regex = r'(?:patchy )?fog'

    if re.fullmatch(rainy_regex, short_forecast):
        return Emojis.Rain
    elif re.fullmatch(cloudy_regex, short_forecast):
        return Emojis.Cloud
    elif re.fullmatch(partly_cloudy_regex, short_forecast):
        if night:
            date = _convert_time_str_to_datetime(period['startTime']).date()
            return get_moon_phase(date) + Emojis.Cloud
        else:
            return Emojis.SunBehindCloud
    elif re.fullmatch(sunny_regex, short_forecast):
        return Emojis.Sun
    elif re.fullmatch(clear_regex, short_forecast) and night:
        return Emojis.NightWithStars
    elif re.fullmatch(thunderstorm_regex, short_forecast):
        return Emojis.RainAndLightning
    elif re.fullmatch(fog_regex, short_forecast):
        return Emojis.Fog
    else:
        return None


def get_weather(client: praw.Reddit) -> str:
    response = requests.get(NWS_FORECAST_URL)
    data = response.json()

    # TODO: I vaguely remember there being a way to get advisories. Can't find it right now for some reason though
    current_date = datetime.date.today()
    tomorrow = current_date + datetime.timedelta(days=1)
    forecast_periods = [period for period in data['properties']['periods']
                        if current_date <= _convert_time_str_to_datetime(period['startTime']).date() <= tomorrow]
    comment_lines = []
    emoji_fails = []

    for period in forecast_periods:
        name, forecast = period['name'], period['detailedForecast']
        try:
            emoji = get_weather_emoji(period)
            if emoji is not None:
                comment_lines.append('* {}: {} {}'.format(name, emoji, forecast))
            else:
                emoji_fails.append(period)
                comment_lines.append('* {}: {}'.format(name, forecast))
        except Exception as e:
            emoji_fails.append(period)
            emoji_fails.append('{}\n{}'.format(e, e.__traceback__))
            comment_lines.append('* {}: {}'.format(name, forecast))

    # We might not have been able to emojify the weather, send a PM so that we can fix it
    if emoji_fails:
        client.redditor('wchill').message(
            'Emojification failed!', json.dumps(emoji_fails))
    return '\n'.join(comment_lines)


def gen_post(weekday: int, client: praw.Reddit) -> str:
    j2_env = Environment(loader=FileSystemLoader(
        './templates'), trim_blocks=True)
    template = j2_env.get_template('daily_post.j2')

    if weekday == 4:  # Friday is Fri-ku-day
        quote_of_the_day = daily_markov.get_haiku(subreddit)
    else:
        quote_of_the_day = daily_markov.get_quote(subreddit)

    try:
        forecast = get_weather(client)
    except Exception as e:  # Lazy catch all exceptions
        print('Error in forecast: {}'.format(e))
        print(e.__traceback__)
        forecast = '{} Could not fetch weather; Government must be shut down.'.format(
            Emojis.FearfulFace)

    return template.render(day_of_week=weekday, forecast=forecast, qotd=quote_of_the_day)


if __name__ == '__main__':
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                         client_secret=REDDIT_CLIENT_SECRET,
                         password=REDDIT_PASSWORD,
                         user_agent=REDDIT_USER_AGENT,
                         username=REDDIT_USERNAME)

    subreddit = reddit.subreddit(REDDIT_SUB)

    now = datetime.datetime.now()
    post = gen_post(now.weekday(), reddit)

    subreddit.submit(title=now.strftime("Seattle Reddit Community Open Chat, %A, %B %d, %Y"),
                     selftext=post,
                     url=None,
                     resubmit=True,
                     send_replies=False)
