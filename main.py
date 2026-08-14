import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# --- SOFORTIGES PORT-BINDING FÜR RENDER ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is online!")
    def log_message(self, format, *args):
        pass

port = int(os.environ.get("PORT", 10000))
server = HTTPServer(("0.0.0.0", port), DummyHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()
# ------------------------------------------

import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import asyncio

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
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False), 
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        
        channel = await guild.create_text_channel(name=f"bewerbung-{interaction.user.name}", category=category, overwrites=overwrites)
        
        embed = discord.Embed(title=f"Bewerbung von {interaction.user.name}")
        embed.add_field(name="Alter", value=self.frage1.value, inline=False)
        embed.add_field(name="Erfahrungen", value=self.frage2.value, inline=False)
        embed.add_field(name="Warum", value=self.frage3.value, inline=False)
        
        await channel.send(embed=embed, view=TicketActionView())

class TicketActionView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Angenommen! Ticket schließt sich...", ephemeral=True)
        await asyncio.sleep(2)
        channel = interaction.channel
        await channel.delete()

    @discord.ui.button(label="Ablehnen", style=discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Abgelehnt! Ticket schließt sich...", ephemeral=True)
        await asyncio.sleep(2)
        channel = interaction.channel
        await channel.delete()

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
