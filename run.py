import helpers
import sys
import requests
from bs4 import BeautifulSoup
from pathlib import Path


def isAlreadyTooted(tweet_id):
    """ Check if a tweet has already been POSTed to Mastodon. If so, let's not do that again.

    This is important!

    Since this script will likely run as a cron, tweet-bombing our favorite Mastodon neighbourhood
    will ruin things for everyone.

    Arguments:
        tweet_id {string} -- Numerical tweet ID returned by getTweets().
    """

    cache_path = helpers._config('toots.cache_path')

    my_file = Path(cache_path + tweet_id)
    if my_file.is_file():

        return True
    else:

        return False


def getTweets():
    """ Get list of tweets, with tweet ID and content, from configured Twitter account URL.

    This function relies on BeautifulSoup to extract the tweet IDs and content of all tweets on the specified page.

    The data is returned as a list of dictionaries that can be used by other functions.
    """

    all_tweets = []

    url = helpers._config('tweets.source_account_url')

    if not url:

        return False

    headers = {}
    headers['accept-language'] = 'en-US,en;q=0.9'
    headers['dnt'] = '1'
    headers['user-agent'] = helpers._config('gen.APP_NAME')

    data = requests.get(url)

    html = BeautifulSoup(data.text, 'html.parser')

    timeline = html.select('#timeline li.stream-item')

    if timeline is None:

        return False

    helpers._info('getTweets => Fetching tweets for ' + url + '.')

    for tweet in timeline:

        tweet_id = tweet['data-item-id']
        tweet_text = tweet.select('p.tweet-text')[0].get_text()

        all_tweets.append({"id": tweet_id, "text": tweet_text})

    return all_tweets if len(all_tweets) > 0 else None


def tootTheTweet(tweet):
    """ Receieve a dictionary containing Tweet ID and text... and TOOT!

    This function relies on the requests library to post the content to your Mastodon account (human or bot).

    A boolean success status is returned.

    Arguments:
        tweet {dictionary} -- Dictionary containing the "id" and "text" of a single tweet.
    """

    if isAlreadyTooted(tweet['id']):

        helpers._info('tootTheTweet => ' +
                      tweet['id'] + ' already tooted. Skipping.')

        return False

    host_instance = helpers._config('toots.host_instance')
    token = helpers._config('toots.app_secure_token')

    headers = {}
    headers['Authorization'] = 'Bearer ' + token
    headers['Idempotency-Key'] = tweet['id']

    data = {}
    data['status'] = tweet['text']
    data['visibility'] = 'public'

    cache_path = '/tmp/' + tweet['id']
    new_days = open(cache_path, 'w')
    new_days.write(tweet['text'])
    new_days.close()

    response = requests.post(
        url=host_instance + '/api/v1/statuses', data=data, headers=headers)

    if response.status_code == 200:

        helpers._info('tootTheTweet => OK (Response: ' + response.text + ')')

        return True

    else:

        helpers._error(
            'tootTheTweet => FAIL (Response: ' + response.text + ')')

        return False


if __name__ == '__main__':

    """ It all starts here...

    This function will get a new Tweet from the configured Twitter account and publish to the configured Mastodon instance.
    It will only toot once per invokation to avoid flooding the instance.
    """

    tweets = getTweets()

    if not tweets:

        helpers._error(
            '__main__ => No tweets fetched. Please check the Twitter account URL "tweets.source_account_url" in the config.json file.')

        sys.exit()

    helpers._info('__main__ => ' + str(len(tweets)) + ' tweets fetched.')

    for tweet in tweets:

        if tootTheTweet(tweet):

            helpers._info('__main__ => Tooted "' + tweet['text'] + '"')
            helpers._info(
                '__main__ => Tooting less is tooting more. Sleeping...')

            sys.exit()
