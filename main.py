import openai
import discord
from discord import app_commands, Intents, Client, Interaction
openai.api_key = "" #https://beta.openai.com/account/api-keys
token = "" #https://discord.com/developers/applications


class ChatGPT(Client):

    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()

client = ChatGPT(intents=Intents.none())

@client.event
async def on_ready():
    print ("Succesfully logged in as user {0.user}".format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="a pasting stream"))


@client.tree.command()
@app_commands.describe(what_to_paste = "What would you want me to paste?")
async def paste(interaction: Interaction, what_to_paste: str):

    print(f">{interaction.user} wanted to paste something.")
    await interaction.response.send_message(f"**Give me a sec, im pasting...**", ephemeral=True)

    arg = what_to_paste
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=arg,
        temperature=0.5,
        max_tokens=1200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    text = response['choices'][0]['text']
    chunks = [text[i:i + 1900] for i in range(0, len(text), 1900)]

    for chunk in chunks:
        await interaction.channel.send(f"**{interaction.user}** said: `{what_to_paste}`\n" + "```" + chunk + "```")

client.run(token)