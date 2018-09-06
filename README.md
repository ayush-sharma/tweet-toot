# Tweet-Toot
Tweet-Toot is a small Python3 script(s) to convert a tweet to a toot. It's basically a Twitter relay for Mastodon.

The way it works is this: Tweet-Toot can "watch" a Twitter account and repost new tweets to any Mastodon account you configure. Just clone this repo, configure the script, add it to a cron job, and it will repost a new content.

## How do I install this?
Getting Tweet-Toot working is pretty easy. Before you can install it, you're going to need the following:

- Pick a Mastodon instance of your choice. You'll need this instance URL.
- Create an app on the Mastodon instance of your choice and generate an access token.
- You'll also need the Twitter URL of the account you want to watch.

Once you have the above, just follow these steps:

1. Clone this repository.
2. Install the Python3 libraries `requests` and `beautifulsoup` mentioned in the `requirements.txt` file.
3. In `config.json`, update `tweets.source_account_url` with the source Twitter account, `toots.host_instance` with the HTTPS URL of your instance, and `toots.app_secure_token` with the access token you generated.

For example:

`tweets.source_account_url` = https://twitter.com/SarcasmMother

`toots.host_instance` = https://botsin.space

`toots.app_secure_token` = XXXXX-XXXXX-XXXXX-XXXXX-XXXXX'


## How do I run it?
Once it's all setup, just run the main file like this:

`python3 run.py`

If all goes well, you'll see something like this:
```bash
Tweet-Toot | 2018-08-20 21:21:52 _info > getTweets => Fetching tweets for https://twitter.com/SarcasmMother.
Tweet-Toot | 2018-08-20 21:21:52 _info > __main__ => 20 tweets fetched.
Tweet-Toot | 2018-08-20 21:21:52 _info > tootTheTweet => 1031383086963994625 already tooted. Skipping.
Tweet-Toot | 2018-08-20 21:21:52 _info > tootTheTweet => 1031382821791657984 already tooted. Skipping.
Tweet-Toot | 2018-08-20 21:21:53 _info > tootTheTweet => OK (Response: {"id":"100583362607805661","created_at":"2018-08-20T15:51:53.284Z","in_reply_to_id":null,"in_reply_to_account_id":null,"sensitive":false,"spoiler_text":"","visibility":"public","language":"en","uri":"https://botsin.space/users/motherofsarcasm/statuses/100583362607805661","content":"\u003cp\u003eYou are paid by how hard you are to replace. Not by how hard you work.\u003c/p\u003e","url":"https://botsin.space/@motherofsarcasm/100583362607805661","reblogs_count":0,"favourites_count":0,"favourited":false,"reblogged":false,"muted":false,"pinned":false,"reblog":null,"application":{"name":"TweetToot","website":""},"account":{"id":"58348","username":"motherofsarcasm","acct":"motherofsarcasm","display_name":"Mother Of Sarcasm","locked":false,"bot":true,"created_at":"2018-08-20T15:07:42.747Z","note":"\u003cp\u003eFOLLOWS YOU\u003c/p\u003e","url":"https://botsin.space/@motherofsarcasm","avatar":"https://files.botsin.space/accounts/avatars/000/058/348/original/658f78e1f07e94fa.jpg","avatar_static":"https://files.botsin.space/accounts/avatars/000/058/348/original/658f78e1f07e94fa.jpg","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":1,"statuses_count":3,"emojis":[],"fields":[{"name":"Name","value":"Mother Of Sarcasm"},{"name":"Owner","value":"ayushsharma22@mastodon.technology"},{"name":"Birdsite","value":"\u003ca href=\"https://twitter.com/SarcasmMother\" rel=\"me nofollow noopener\" target=\"_blank\"\u003e\u003cspan class=\"invisible\"\u003ehttps://\u003c/span\u003e\u003cspan class=\"\"\u003etwitter.com/SarcasmMother\u003c/span\u003e\u003cspan class=\"invisible\"\u003e\u003c/span\u003e\u003c/a\u003e"}]},"media_attachments":[],"mentions":[],"tags":[],"emojis":[]})
Tweet-Toot | 2018-08-20 21:21:53 _info > __main__ => Tooted "You are paid by how hard you are to replace. Not by how hard you work."
Tweet-Toot | 2018-08-20 21:21:53 _info > __main__ => Tooting less is tooting more. Sleeping...
```

## Things to remember
- The script is designed to toot once per invokation. I recommend timing your cron jobs according to the post frequency that you need instead of modifying the code.
- Mastodon instance admins are people too. Don't toot-blast your instance and make life harder for them.
- When configuring your bot, ensure you clearly display an account where you can be reached in case of issues.

Have fun :)