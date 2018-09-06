# Tweet-Toot
Tweet-Toot is a small Python3 project to convert a tweet to a toot. It's basically a Twitter relay for Mastodon.

The way it works is this: add Tweet-Toot as a cron job, and it will repost new tweets to any Mastodon account you configure. Just clone this repo, configure the script, add it to a cron job, and it will get cracking.

## How do I install this?
Getting Tweet-Toot working is pretty easy. Before you can install it, you're going to need to do the following:

- Pick a Mastodon instance of your choice. You'll need this instance's URL.
- Create an app on this Mastodon instance and generate an access token.
- Get the Twitter URL of the account you want to watch.

Once you have the above, just follow these steps:

1. Clone this repository.
2. Install the Python3 libraries `requests` and `beautifulsoup` mentioned in the `requirements.txt` file.
3. In `config.json`, update the following:

- `tweets.source_account_url`: The source Twitter account.
- `toots.host_instance`: The HTTPS URL of your instance.
- `toots.app_secure_token`: The Mastodon app access token.

For example:

- `tweets.source_account_url` = https://twitter.com/SarcasmMother
- `toots.host_instance` = https://botsin.space
- `toots.app_secure_token` = XXXXX-XXXXX-XXXXX-XXXXX-XXXXX'


## How do I run it?
Once it's all setup, just run the main file like this:

`python3 run.py`

If all goes well, you'll see something like this:
```bash
Tweet-Toot | 2018-09-06 22:59:10 _info > getTweets() => Fetched tweets for https://twitter.com/SarcasmMother.
Tweet-Toot | 2018-09-06 22:59:10 _info > __main__ => 20 tweets fetched.
Tweet-Toot | 2018-09-06 22:59:10 _info > tootTheTweet() => Tweet 1031642593594028032 was already posted. Skipping...
Tweet-Toot | 2018-09-06 22:59:10 _info > tootTheTweet() => Tweet 1031640753187958786 was already posted. Skipping...
Tweet-Toot | 2018-09-06 22:59:10 _info > tootTheTweet() => Tweet 1031632691500789761 was already posted. Skipping...
Tweet-Toot | 2018-09-06 22:59:10 _info > tootTheTweet() => New tweet 1031572182114004993 => "You discovered the ability to time travel. You go 30 years into the future expecting to meet your future self only to discover that you've been missing for 30 years.".
Tweet-Toot | 2018-09-06 22:59:11 _info > tootTheTweet() => OK. Posted tweet 1031572182114004993to Mastodon.
Tweet-Toot | 2018-09-06 22:59:11 _info > tootTheTweet() => Response: {"id":"100680004506399841","created_at":"2018-09-06T17:29:11.674Z","in_reply_to_id":null,"in_reply_to_account_id":null,"sensitive":false,"spoiler_text":"","visibility":"public","language":"en","uri":"https://botsin.space/users/motherofsarcasm/statuses/100680004506399841","content":"\u003cp\u003eYou discovered the ability to time travel. You go 30 years into the future expecting to meet your future self only to discover that you\u0026apos;ve been missing for 30 years.\u003c/p\u003e","url":"https://botsin.space/@motherofsarcasm/100680004506399841","replies_count":0,"reblogs_count":0,"favourites_count":0,"favourited":false,"reblogged":false,"muted":false,"pinned":false,"reblog":null,"application":{"name":"TweetToot","website":""},"account":{"id":"-----","username":"motherofsarcasm","acct":"motherofsarcasm","display_name":"Mother Of Sarcasm","locked":false,"bot":true,"created_at":"2018-08-20T15:07:42.747Z","note":"\u003cp\u003eFOLLOWS YOU\u003c/p\u003e","url":"https://botsin.space/@motherofsarcasm","avatar":"https://files.botsin.space/accounts/avatars/000/058/348/original/658f78e1f07e94fa.jpg","avatar_static":"https://files.botsin.space/accounts/avatars/000/058/348/original/658f78e1f07e94fa.jpg","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":1,"statuses_count":7,"emojis":[],"fields":[{"name":"Name","value":"Mother Of Sarcasm"},{"name":"Owner","value":"ayushsharma22@mastodon.technology"},{"name":"Twitter Relay","value":"\u003ca href=\"https://twitter.com/SarcasmMother\" rel=\"me nofollow noopener\" target=\"_blank\"\u003e\u003cspan class=\"invisible\"\u003ehttps://\u003c/span\u003e\u003cspan class=\"\"\u003etwitter.com/SarcasmMother\u003c/span\u003e\u003cspan class=\"invisible\"\u003e\u003c/span\u003e\u003c/a\u003e"}]},"media_attachments":[],"mentions":[],"tags":[],"emojis":[]}
Tweet-Toot | 2018-09-06 22:59:11 _info > __main__ => Tooted "You discovered the ability to time travel. You go 30 years into the future expecting to meet your future self only to discover that you've been missing for 30 years."
Tweet-Toot | 2018-09-06 22:59:11 _info > __main__ => Tooting less is tooting more. Sleeping...

```

## Things to remember
- The script is designed to toot once per invokation. I recommend timing your cron jobs according to the post frequency that you need instead of modifying the code.
- Mastodon instance admins are people too. Don't toot-blast your instance and make life harder for them.
- When configuring your bot, ensure you clearly display an account where you can be reached in case of issues.

Have fun :)