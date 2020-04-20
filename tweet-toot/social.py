#!/usr/bin/env python3

import base64
import logging
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import helpers

logger = logging.getLogger(__name__)


def get_tweets():
    """ Get list of tweets, with tweet ID and content, from configured Twitter account URL.

    This function relies on BeautifulSoup to extract the tweet IDs and content of all tweets on the specified page.

    The data is returned as a list of dictionaries that can be used by other functions.
    """

    all_tweets = []
    url = helpers._config("TT_SOURCE_TWITTER_URL")

    if not url:
        logger.error(
            f"get_tweets() => The source Twitter account URL ({url}) was incorrect. Could not retrieve tweets."
        )
        return False

    headers = {}
    headers["accept-language"] = "en-US,en;q=0.9"
    headers["dnt"] = "1"
    headers["user-agent"] = helpers._config("TT_APP_NAME")

    data = requests.get(url)
    html = BeautifulSoup(data.text, "html.parser")
    timeline = html.select("#timeline li.stream-item")

    if timeline is None:
        logger.error(
            f"get_tweets() => Could not retrieve tweets from the page. Please make sure the source Twitter account URL ({url}) is correct."
        )
        return False

    logger.info(f"get_tweets() => Fetched tweets for {url}.")

    for tweet in timeline:

        try:

            tweet_id = tweet["data-item-id"]
            tweet_text = tweet.select("p.tweet-text")[0].get_text().encode("utf-8")
            tweet_time = int(tweet.select("span._timestamp")[0].attrs["data-time-ms"])

            all_tweets.append({"id": tweet_id, "text": tweet_text, "time": tweet_time})

        except Exception as e:

            logger.error("get_tweets() => No tweet text found.")
            logger.error(e)
            continue

    return all_tweets if len(all_tweets) > 0 else None


def toot_the_tweet(tweet):
    """ Receieve a dictionary containing Tweet ID and text... and TOOT!

    This function relies on the requests library to post the content to your Mastodon account (human or bot).

    A boolean success status is returned.

    Arguments:
        tweet {dictionary} -- Dictionary containing the "id" and "text" of a single tweet.
    """

    host_instance = helpers._config("TT_HOST_INSTANCE")
    token = helpers._config("TT_APP_SECURE_TOKEN")
    timestamp_file = helpers._config("TT_CACHE_PATH") + "last_tweet_tooted"

    if not host_instance:
        logger.error(
            f"toot_the_tweet() => Your host Mastodon instance URL ({host_instance}) was incorrect."
        )
        return False

    if not token:
        logger.error("toot_the_tweet() => Your Mastodon access token was incorrect.")
        return False

    last_timestamp = helpers._read_file(timestamp_file)
    if not last_timestamp:

        helpers._write_file(timestamp_file, str(tweet["time"]))

        return False

    last_timestamp = int(last_timestamp)

    headers = {}
    headers["Authorization"] = f"Bearer {token}"
    headers["Idempotency-Key"] = tweet["id"]

    data = {}
    data["status"] = tweet["text"]
    data["visibility"] = "public"

    if tweet["time"] <= last_timestamp:

        logger.info("toot_the_tweet() => No new tweets. Moving on.")

        return None

    last_timestamp = helpers._write_file(timestamp_file, str(tweet["time"]))

    logger.info(f'toot_the_tweet() => New tweet {tweet["id"]} => "{tweet["text"]}".')

    response = requests.post(
        url=f"{host_instance}/api/v1/statuses", data=data, headers=headers
    )

    if response.status_code == 200:
        logger.info(f"toot_the_tweet() => OK. Posted tweet {tweet['id']} to Mastodon.")
        logger.info(f"toot_the_tweet() => Response: {response.text}")
        return True

    else:
        logger.info(
            f"toot_the_tweet() => FAIL. Could not post tweet {tweet['id']} to Mastodon."
        )
        logger.info(f"toot_the_tweet() => Response: {response.text}")
        return False
