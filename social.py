import helpers
import requests
from bs4 import BeautifulSoup
from pathlib import Path


def getTweets():
    """ Get list of tweets, with tweet ID and content, from configured Twitter account URL.

    This function relies on BeautifulSoup to extract the tweet IDs and content of all tweets on the specified page.

    The data is returned as a list of dictionaries that can be used by other functions.
    """

    all_tweets = []

    url = helpers._config('tweets.source_account_url')

    if not url:

        helpers._error('getTweets() => The source Twitter account URL (' + url + ') was incorrect. Could not retrieve tweets.')

        return False

    headers = {}
    headers['accept-language'] = 'en-US,en;q=0.9'
    headers['dnt'] = '1'
    headers['user-agent'] = helpers._config('gen.APP_NAME')

    data = requests.get(url)

    html = BeautifulSoup(data.text, 'html.parser')

    timeline = html.select('#timeline li.stream-item')

    if timeline is None:

        helpers._error('getTweets() => Could not retrieve tweets from the page. Please make sure the source Twitter account URL (' + url + ') is correct.')

        return False

    helpers._info('getTweets() => Fetched tweets for ' + url + '.')

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

    host_instance = helpers._config('toots.host_instance')
    token = helpers._config('toots.app_secure_token')

    tweet_id = tweet['id']

    if not host_instance:

        helpers._error('tootTheTweet() => Your host Mastodon instance URL (' + host_instance + ') was incorrect.')

        return False

    if not token:

        helpers._error('tootTheTweet() => Your Mastodon access token was incorrect.')

        return False  

    headers = {}
    headers['Authorization'] = 'Bearer ' + token
    headers['Idempotency-Key'] = tweet_id

    data = {}
    data['status'] = tweet['text']
    data['visibility'] = 'public'

    tweet_check_file_path = helpers._config('toots.cache_path') + tweet['id']
    tweet_check_file = Path(tweet_check_file_path)
    if tweet_check_file.is_file():

        helpers._info('tootTheTweet() => Tweet ' + tweet_id + ' was already posted. Reposting...')

    else:

        tweet_check = open(tweet_check_file_path, 'w')
        tweet_check.write(tweet['text'])
        tweet_check.close()

        helpers._info('tootTheTweet() => New tweet ' + tweet_id + ' => "' + tweet['text'] + '".')    

    response = requests.post(
        url=host_instance + '/api/v1/statuses', data=data, headers=headers)

    if response.status_code == 200:

        helpers._info('tootTheTweet() => OK. Posted tweet ' + tweet_id + 'to Mastodon.')
        helpers._info('tootTheTweet() => Response: ' + response.text)

        return True

    else:

        helpers._info('tootTheTweet() => FAIL. Could not post tweet ' + tweet_id + 'to Mastodon.')
        helpers._info('tootTheTweet() => Response: ' + response.text)

        return False