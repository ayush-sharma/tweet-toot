#!/usr/bin/env python3

import encodings.idna
import logging
import sys

import helpers
import social

if __name__ == "__main__":

    """ It all starts here...

    This function will get a new Tweet from the configured Twitter account and publish to the configured Mastodon instance.
    It will only toot once per invokation to avoid flooding the instance.
    """

    # Initialize common logging options
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    tweets = social.get_tweets()

    if not tweets:
        logger.error("__main__ => No tweets fetched.")

    else:

        logger.info(f"__main__ => {len(tweets)} tweets fetched.")

        for tweet in tweets:
            if social.toot_the_tweet(tweet):
                logger.info(f'__main__ => Tooted "{tweet["text"]}"')
                logger.info("__main__ => Tooting less is tooting more. Sleeping...")
                sys.exit()
