#!/usr/bin/env python3

import logging
from collections import OrderedDict
from hashlib import sha1

import requests
from bs4 import BeautifulSoup

import helpers

logger = logging.getLogger(__name__)


class TweetToot:

    app_name = ""
    twitter_url = ""
    mastodon_url = ""
    mastodon_token = ""

    def __init__(
        self, app_name: str, twitter_url: str, mastodon_url: str, mastodon_token: str
    ):

        self.app_name = app_name
        self.twitter_url = twitter_url
        self.mastodon_url = mastodon_url
        self.mastodon_token = mastodon_token

    def relay(self):

        """ Main code which relays tweets to the Mastodon instance.

        :type self:
        :param self:
    
        :raises:
    
        :rtype: bool
        """

        if not self.app_name:

            logger.error(f"relay() => Application name in config is incorrect/empty.")

            return False

        if not self.twitter_url:

            logger.error(f"relay() => Twitter URL in config is incorrect/empty.")

            return False

        if not self.mastodon_url:

            logger.error(f"relay() => Mastodon URL in config is incorrect/empty.")

            return False

        if not self.mastodon_token:

            logger.error(f"relay() => Mastodon token in config is incorrect/empty.")

            return False

        logger.info(
            f"relay() => Init relay from {self.twitter_url} to {self.mastodon_url}. State file {self._get_timestamp_file_path()}"
        )

        tweets = self._get_tweets()

        if not tweets:

            return True

        logger.debug(f"relay() => {str(tweets)}")

        last_timestamp = 0

        for tweet_time, tweet in tweets.items():

            logger.info(f"relay() => Tweeting {tweet['id']} to {self.mastodon_url}")

            last_timestamp = (
                tweet_time if tweet_time > last_timestamp else last_timestamp
            )

            self._toot_the_tweet(
                mastodon_url=self.mastodon_url,
                tweet_id=tweet["id"],
                tweet_body=tweet["text"],
                tweet_time=tweet_time,
            )

        self._set_last_timestamp(timestamp=last_timestamp)

    def _get_tweets(self):

        """ Get list of new tweets, with tweet ID and content, from configured Twitter account URL.
        This function relies on BeautifulSoup to extract the tweet IDs and content of all tweets on the specified page.
        The data is returned as a list of dictionaries that can be used by other functions.

        :type self:
        :param self:

        :raises:

        :rtype: dict
        """

        tweets = OrderedDict()
        last_timestamp = self._get_last_timestamp()

        headers = {}
        headers["accept-language"] = "en-US,en;q=0.9"
        headers["dnt"] = "1"
        headers["user-agent"] = self.app_name

        data = requests.get(self.twitter_url)
        html = BeautifulSoup(data.text, "html.parser")
        timeline = html.select("#timeline li.stream-item")

        if timeline is None:

            logger.error(
                f"get_tweets() => Could not retrieve tweets from the page. Please make sure the source Twitter URL ({self.twitter_url}) is correct."
            )
            return False

        logger.info(
            f"get_tweets() => Fetched {len(timeline)} tweets for {self.twitter_url}."
        )

        for tweet in timeline:

            try:

                tweet_time = int(
                    tweet.select("span._timestamp")[0].attrs["data-time-ms"]
                )

                if tweet_time > last_timestamp:

                    tweet_id = tweet["data-item-id"]
                    tweet_text = (
                        tweet.select("p.tweet-text")[0].get_text().encode("utf-8")
                    )

                    tweets[tweet_time] = {"id": tweet_id, "text": tweet_text}

            except Exception as e:

                logger.error("get_tweets() => An error occurred.")
                logger.error(e)

                continue

        return (
            {k: tweets[k] for k in sorted(tweets, reverse=True)}
            if len(tweets) > 0
            else None
        )

    def _get_last_timestamp(self):

        """ Get the last tweet's timestamp.

        :type self:
        :param self:

        :raises:

        :rtype: int
        """

        ts = helpers._read_file(self._get_timestamp_file_path())

        return int(ts) if ts else 0

    def _set_last_timestamp(self, timestamp: int):

        """ Set the last tweet's timestamp.

        :type self:
        :param self:

        :type timestamp:int:
        :param timestamp:int: Timestamp of current tweet.

        :raises:

        :rtype: bool
        """

        return helpers._write_file(self._get_timestamp_file_path(), str(timestamp))

    def _get_timestamp_file_path(self):

        """ Get file path that stores tweet timestamp.

        :type self:
        :param self:

        :raises:

        :rtype: str
        """

        return (
            helpers._config("TT_CACHE_PATH")
            + "tt_"
            + sha1(
                self.twitter_url.encode("utf-8") + self.mastodon_url.encode("utf-8")
            ).hexdigest()
        )

    def _toot_the_tweet(
        self, mastodon_url: str, tweet_id: str, tweet_body: str, tweet_time: int
    ):

        """ Receieve a dictionary containing Tweet ID and text... and TOOT!
        This function relies on the requests library to post the content to your Mastodon account (human or bot).
        A boolean success status is returned.
            
        :type self:
        :param self:
    
        :type tweet_id:str:
        :param tweet_id:str: Tweet ID.
    
        :type tweet_body:str:
        :param tweet_body:str: Tweet text.
    
        :type tweet_time:int:
        :param tweet_time:int: Tweet timestamp.

        :raises:
    
        :rtype: bool
        """

        headers = {}
        headers["Authorization"] = f"Bearer {self.mastodon_token}"
        headers["Idempotency-Key"] = tweet_id

        data = {}
        data["status"] = tweet_body
        data["visibility"] = "public"

        response = requests.post(
            url=f"{mastodon_url}/api/v1/statuses", data=data, headers=headers
        )

        if response.status_code == 200:

            logger.info(
                f"toot_the_tweet() => OK. Tooted {tweet_id} to {self.mastodon_url}."
            )
            logger.debug(f"toot_the_tweet() => Response: {response.text}")

            return True

        else:

            logger.error(
                f"toot_the_tweet() => Could not toot {tweet_id} to {self.mastodon_url}."
            )
            logger.debug(f"toot_the_tweet() => Response: {response.text}")

            return False
