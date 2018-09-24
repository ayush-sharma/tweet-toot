import encodings.idna
import helpers
import social
import sys


if __name__ == '__main__':

    """ It all starts here...

    This function will get a new Tweet from the configured Twitter account and publish to the configured Mastodon instance.
    It will only toot once per invokation to avoid flooding the instance.
    """

    tweets = social.getTweets()

    if not tweets:

        helpers._error(
            '__main__ => No tweets fetched.')

        sys.exit()

    helpers._info('__main__ => ' + str(len(tweets)) + ' tweets fetched.')

    for tweet in tweets:

        if social.tootTheTweet(tweet):

            helpers._info('__main__ => Tooted "' + tweet['text'] + '"')
            helpers._info(
                '__main__ => Tooting less is tooting more. Sleeping...')

            sys.exit()
