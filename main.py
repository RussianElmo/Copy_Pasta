import random
import praw
import configparser
from discord.ext import commands


async def reddit(query, ctx):
    config.read('auth.ini')
    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')
    username = config.get('credentials', 'username')
    password = config.get('credentials', 'password')
    user_agent = 'windows:example.Copy_Pasta.Copy_Pasta:v1.0 (by u/Russian_Elmo)'

    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, username=username, password=password,
                         user_agent=user_agent)

    subreddit = reddit.subreddit('copypasta')

    posts = []

    for post in subreddit.search(query):
        posts.append(post.selftext)
    try:
        to_send = random.choice(posts)
        await ctx.send(to_send)
    except IndexError:
        if len(query) > 1:
            i = 0
            while i < len(query) - 1:
                for post in subreddit.search(query[i]):
                    posts.append(post.selftext)
                if len(posts) > 0:
                    to_send = random.choice(posts)
                    ctx.send(to_send)
                    return
                i += 1
        await ctx.send('Could not find a copypasta with this query')
    except:
        cache = to_send
        while len(to_send) > 2000:
            cache = to_send[:2000]
            await ctx.send(cache)
            to_send = to_send[2000:]
        if len(to_send) > 0:
            await ctx.send(to_send)


config = configparser.ConfigParser()
config.read('auth.ini')

TOKEN = config.get('credentials', 'token')

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print(f'{client.user} has connected to discord')


@client.command()
async def prop(ctx, *args):
    await reddit(args, ctx)



client.run(TOKEN)
