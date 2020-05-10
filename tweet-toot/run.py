#!/usr/bin/env python3

import logging
import sys

import helpers
import tweettoot

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

    # Initialize variables
    app_name = helpers._config("TT_APP_NAME")
    separator = ","
    twitter_url = helpers._config("TT_SOURCE_TWITTER_URL").split(separator)
    mastodon_url = helpers._config("TT_HOST_INSTANCE").split(separator)
    mastodon_token = helpers._config("TT_APP_SECURE_TOKEN").split(separator)
    cache_path = helpers._config("TT_CACHE_PATH")
    mode = helpers._config("TT_MODE")

    if len(mastodon_url) != len(mastodon_token):

        logger.error(
            "Lenghts of Mastodon URL ({}) and Mastodon tokens ({}) do not match.".format(len(mastodon_url), len(mastodon_url))
        )

    else:

        logger.info("__main__ => Mode: {}".format(mode))

        if mode == "one-to-one":

            # In this mode, the first Twitter URL is picked and it is relayed to the first Mastodon URL/Token combination. This repeats until we run out of Twitter URLs or Mastodon URLs. The number of Twitter accounts must be equal to the number of Mastodon URLs/tokens to avoid wierdness.

            if len(twitter_url) != len(mastodon_url):

                logger.error(
                    "In {}, the number of Twitter URLs and Mastodon hosts should be the same.".format(mode)
                )

                sys.exit(0)

            for index_t, url_t in enumerate(twitter_url):

                job = tweettoot.TweetToot(
                    app_name=app_name,
                    twitter_url=url_t,
                    mastodon_url=mastodon_url[index_t],
                    mastodon_token=mastodon_token[index_t],
                )

                job.relay()

            sys.exit(0)

        elif mode == "one-to-many":

            # In this mode, the first Twitter URL is picked and relayed to all Mastodon instances. Then the next Twitter URL is picked.

            if len(twitter_url) == 1:

                logger.error("In {}, there can only be 1 Twitter URL.".format(mode))

                sys.exit(0)

        elif mode == "many-to-one":

            # In this mode, every Twitter account is relayed to a single Mastodon instance.

            if len(mastodon_url) != 1:

                logger.error("In {}, there can only be 1 Mastodon host.".format(mode))

                sys.exit(0)

        elif mode == "many-to-many":

            # In this mode, every Twitter account is relayed to all Mastodon instances.

            pass

        else:

            logger.critical("__main__ => {} incorrect.".format(mode))

            sys.exit(0)

        for index_t, url_t in enumerate(twitter_url):

            for index_m, url_m in enumerate(mastodon_url):

                job = tweettoot.TweetToot(
                    app_name=app_name,
                    twitter_url=url_t,
                    mastodon_url=url_m,
                    mastodon_token=mastodon_token[index_m],
                )

                job.relay()
