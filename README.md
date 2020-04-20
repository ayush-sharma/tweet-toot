# Tweet-Toot
Tweet-Toot is a small Python3 project to convert a tweet to a toot.

It's basically a Twitter relay for Mastodon :)
 
Just clone it, configure it, schedule it, and it will toot new tweets at a Mastodon of your choice.

---

## How do I install this?
Getting Tweet-Toot working is pretty easy. Before you can install it, you're going to need to do the following:

- Pick a Mastodon instance of your choice. You'll need this instance's URL.
- Create an app on this Mastodon instance and generate an access token.
- Get the Twitter URL of the account you want to watch.

Once you have the above, just follow these steps:

1. Clone this repository.
2. Install the Python3 libraries by running these commands:

 - `python3 -m venv venv`
 - `source venv/bin/activate`
 - `pip3 install -r tweet-toot/requirements.txt`

3. In `config.json`, update the following:

- `TT_SOURCE_TWITTER_URL`: The Twitter account URL.
- `TT_HOST_INSTANCE`: The Mastodon instance URL.
- `TT_APP_SECURE_TOKEN`: The Mastodon app access token.
- `TT_CACHE_PATH`: Cache path. This is where we keep the last tweet, so keep this fixed.

For example:

- `TT_SOURCE_TWITTER_URL` = https://twitter.com/internetofshit
- `TT_HOST_INSTANCE` = https://botsin.space
- `TT_APP_SECURE_TOKEN` = XXXXX-XXXXX-XXXXX-XXXXX-XXXXX'
- `TT_CACHE_PATH` = `/tmp`

---

## How do I run it?
Once it's all setup, execute the app by running:

```bash
source venv/bin/activate
cd tweet-toot
python run.py
```

If all goes well, you'll see something like this:
```bash
2020-04-20 17:42:45,880 - social - INFO - get_tweets() => Fetched tweets for https://twitter.com/internetofshit.
2020-04-20 17:42:45,976 - __main__ - INFO - __main__ => 20 tweets fetched.
2020-04-20 17:42:45,977 - social - INFO - toot_the_tweet() => New tweet 1251661782457991168 => "b'This thread starts out as some innocent  hacking and ends up with a bunch of HTTP servers running on a tv remote https://twitter.com/Foone/status/1251395931351609347\xc2\xa0\xe2\x80\xa6'".
2020-04-20 17:42:47,142 - social - INFO - toot_the_tweet() => OK. Posted tweet 1251661782457991168 to Mastodon.
2020-04-20 17:42:47,142 - social - INFO - toot_the_tweet() => Response: {"id":"104032145682490500","created_at":"2020-04-20T17:42:46.777Z","in_reply_to_id":null,"in_reply_to_account_id":null,"sensitive":false,"spoiler_text":"","visibility":"public","language":"en","uri":"https://botsin.space/users/motherofsarcasm/statuses/104032145682490500","url":"https://botsin.space/@motherofsarcasm/104032145682490500","replies_count":0,"reblogs_count":0,"favourites_count":0,"favourited":false,"reblogged":false,"muted":false,"bookmarked":false,"pinned":false,"content":"\u003cp\u003eThis thread starts out as some innocent  hacking and ends up with a bunch of HTTP servers running on a tv remote \u003ca href=\"https://twitter.com/Foone/status/1251395931351609347\" rel=\"nofollow noopener noreferrer\" target=\"_blank\"\u003e\u003cspan class=\"invisible\"\u003ehttps://\u003c/span\u003e\u003cspan class=\"ellipsis\"\u003etwitter.com/Foone/status/12513\u003c/span\u003e\u003cspan class=\"invisible\"\u003e95931351609347\u003c/span\u003e\u003c/a\u003e …\u003c/p\u003e","reblog":null,"application":{"name":"TweetToot","website":""},"account":{"id":"58348","username":"motherofsarcasm","acct":"motherofsarcasm","display_name":"Mother Of Sarcasm","locked":false,"bot":true,"discoverable":null,"group":false,"created_at":"2018-08-20T15:07:42.747Z","note":"\u003cp\u003eFOLLOWS YOU\u003c/p\u003e","url":"https://botsin.space/@motherofsarcasm","avatar":"https://files.botsin.space/accounts/avatars/000/058/348/original/658f78e1f07e94fa.jpg","avatar_static":"https://files.botsin.space/accounts/avatars/000/058/348/original/658f78e1f07e94fa.jpg","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":3,"following_count":1,"statuses_count":1156,"last_status_at":"2020-04-20","emojis":[],"fields":[{"name":"Name","value":"Mother Of Sarcasm","verified_at":null},{"name":"Owner","value":"ayushsharma22@mastodon.technology","verified_at":null},{"name":"Twitter Relay","value":"\u003ca href=\"https://twitter.com/SarcasmMother\" rel=\"me nofollow noopener noreferrer\" target=\"_blank\"\u003e\u003cspan class=\"invisible\"\u003ehttps://\u003c/span\u003e\u003cspan class=\"\"\u003etwitter.com/SarcasmMother\u003c/span\u003e\u003cspan class=\"invisible\"\u003e\u003c/span\u003e\u003c/a\u003e","verified_at":null}]},"media_attachments":[],"mentions":[],"tags":[],"emojis":[],"card":null,"poll":null}
2020-04-20 17:42:47,142 - __main__ - INFO - __main__ => Tooted "b'This thread starts out as some innocent  hacking and ends up with a bunch of HTTP servers running on a tv remote https://twitter.com/Foone/status/1251395931351609347\xc2\xa0\xe2\x80\xa6'"
2020-04-20 17:42:47,142 - __main__ - INFO - __main__ => Tooting less is tooting more. Sleeping...
```

---

## How does it work?
The tutorial for this code can be found here: [Tweet-Toot: Building a bot for Mastodon using Python](https://notes.ayushsharma.in/2018/09/tweet-toot-building-a-bot-for-mastodon-using-python).

If you like the tutorial, don't forget to spread the word on Mastodon :)

---

## How do I build the Docker image and run it?
I've added a `Dockerfile` with this repo so you can get up and running with Docker quickly.

### To build the Docker image locally:

1. Clone this repo.
   
2. In the main directory, run:
   
   ```
   docker build -t tweet-toot:latest -f Dockerfile tweet-toot
   ```

3. Export your Mastodon token in your environment:
   
   ```
   export TT_APP_SECURE_TOKEN="<token>"
   ```

   We'll pass this to the container later. No need to hard-code the `config.json`.

4. Execute the container:
   
   ```
   docker run --rm -e TT_APP_SECURE_TOKEN="$TT_APP_SECURE_TOKEN" -v /tmp:/tmp tweet-toot:latest
   ```

   We need `TT_CACHE_PATH` same across `docker run`s, so we're mounting a local directory into the container's `/tmp`. Customise as you see fit.
   
   To override more config paramters, just pass more `-e`s to Docker.

---

## Things to remember
- The script is designed to toot once per invokation. I recommend timing your cron jobs according to the post frequency that you need instead of modifying the code.
- Mastodon instance admins are people too. Don't toot-blast your instance and make life harder for them.
- When configuring your bot, ensure you clearly display an account where you can be reached in case of issues.

Have fun :)

---

For questions or contributions, please create an issue.

You can find me on [Mastodon](https://mastodon.technology/@ayushsharma22) or [ayushsharma.in](https://ayushsharma.in).