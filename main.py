import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import asyncio
import os

# TRAGE HIER DEINE ID EIN:
OWNER_ID = 1523728380476919910 

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

class BewerbungsModal(Modal, title="Bewerbungsformular"):
    frage1 = TextInput(label="Alter / Angaben", placeholder="Dein Alter...", required=True)
    frage2 = TextInput(label="Erfahrungen", placeholder="Deine Erfahrungen...", style=discord.TextStyle.paragraph, required=True)
    frage3 = TextInput(label="Warum wir?", placeholder="Deine Motivation...", style=discord.TextStyle.paragraph, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Bewerbung wird erstellt...", ephemeral=True)
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Bewerbungen") or await guild.create_category("Bewerbungen")
        
        overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False), 
                      interaction.user: discord.PermissionOverwrite(read_messages=True),
                      guild.me: discord.PermissionOverwrite(read_messages=True)}
        
        channel = await guild.create_text_channel(name=f"bewerbung-{interaction.user.name}", category=category, overwrites=overwrites)
        
        embed = discord.Embed(title=f"Bewerbung von {interaction.user.name}")
        embed.add_field(name="Alter", value=self.frage1.value, inline=False)
        embed.add_field(name="Erfahrungen", value=self.frage2.value, inline=False)
        embed.add_field(name="Warum", value=self.frage3.value, inline=False)
        
        await channel.send(embed=embed, view=TicketActionView(interaction.user.id))

class TicketActionView(View):
    def __init__(self, target_id):
        super().__init__(timeout=None)
        self.target_id = target_id

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message("Nur der Inhaber!", ephemeral=True)
        await interaction.response.send_message("Angenommen! Ticket schließt sich...", ephemeral=True)
        await asyncio.sleep(2)
        await interaction.channel.delete()

    @discord.ui.button(label="Ablehnen", style=discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message("Nur der Inhaber!", ephemeral=True)
        await interaction.response.send_message("Abgelehnt! Ticket schließt sich...", ephemeral=True)
        await asyncio.sleep(2)
        await interaction.channel.delete()

class BewerungsStartView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Bewerbung abschicken", style=discord.ButtonStyle.blurple, custom_id="open_bewerbung")
    async def open_modal(self, interaction, button):
        await interaction.response.send_modal(BewerbungsModal())

@bot.event
async def on_ready():
    bot.add_view(BewerungsStartView())
    print("Bot ist bereit!")

@bot.tree.command(name="ticket")
async def ticket(interaction: discord.Interaction):
    await interaction.channel.send("Klicke unten für die Bewerbung:", view=BewerungsStartView())
    await interaction.response.send_message("Panel gesendet!", ephemeral=True)

bot.run(os.getenv("TOKEN"))
