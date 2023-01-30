# Twitter CatBot

The code for https://twitter.com/CatBot42

Because one cat per day keeps the doctor away.

## Deployment

- Create a Cat Api key [here](https://thecatapi.com/)
- Create a [Twitter Developer Account](https://developer.twitter.com/en/portal/dashboard)
- Create an `env.json` file with the cat api, the twitter key and the twitter secret.
- Run `python authenticate.py` and follow instructions.
- Add `twitter_token_key` and `twitter_token_secret` to the env.json
- Add script e.g. to crontab: 

```
0 12 * * * cd ~/catbottwitter && flock -n /tmp/catbottwitter.lockfile python3 main.py
```