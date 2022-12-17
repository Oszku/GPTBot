import openai
import discord
openai.api_key = "" # https://beta.openai.com/account/api-keys
token = '' # https://discord.com/developers/applications
client = discord.Client()

@client.event
async def on_ready():
    print ("Succesfully logged in as user {0.user}".format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="$paste"))

@client.event
async def on_message(message):
    if message.content.startswith("$paste"):
        arg = message.content[7:]
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=arg,
        temperature=0.5,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        await message.channel.send("```" + response['choices'][0]['text'] + "```")

client.run(token)