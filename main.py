import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import asyncio

# --- SCHNELLER WEB-SERVER FÜR RENDER (Lässt den Bot online) ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def log_message(self, format, *args):
        pass

def start_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=start_server, daemon=True).start()
# ------------------------------------------------------------

# DEINE ROLLEN-IDS (Hier eingetragen)
ROLLE_1_ID = 153790247117783592
ROLLE_2_ID = 1537853690076200980

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
        
        embed = discord.Embed(title=f"Bewerbung von {interaction.user.name}", color=discord.Color.blue())
        embed.add_field(name="Alter", value=self.frage1.value, inline=False)
        embed.add_field(name="Erfahrungen", value=self.frage2.value, inline=False)
        embed.add_field(name="Warum", value=self.frage3.value, inline=False)
        
        # Übergibt die ID des Bewerbers an die Buttons
        await channel.send(embed=embed, view=TicketActionView(interaction.user.id))

class TicketActionView(View):
    def __init__(self, target_id: int):
        super().__init__(timeout=None)
        self.target_id = target_id

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        member = guild.get_member(self.target_id)
        if not member:
            try:
                member = await guild.fetch_member(self.target_id)
            except:
                member = None

        # Rollen vergeben
        if member:
            try:
                role1 = guild.get_role(ROLLE_1_ID)
                role2 = guild.get_role(ROLLE_2_ID)
                if role1: 
                    await member.add_roles(role1)
                if role2: 
                    await member.add_roles(role2)
            except Exception as e:
                print(f"Fehler beim Rollen geben: {e}")

            # DM senden
            try:
                await member.send("🎉 Herzlichen Glückwunsch! Deine Bewerbung wurde **angenommen**.")
            except:
                pass

        await interaction.response.send_message("Angenommen! Rollen vergeben und DM gesendet. Ticket schließt sich...", ephemeral=True)
        await asyncio.sleep(2)
        try:
            await interaction.channel.delete()
        except:
            pass

    @discord.ui.button(label="Ablehnen", style=discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        member = guild.get_member(self.target_id)
        if not member:
            try:
                member = await guild.fetch_member(self.target_id)
            except:
                member = None

        # DM senden
        if member:
            try:
                await member.send("❌ Leider wurde deine Bewerbung **abgelehnt**.")
            except:
                pass

        await interaction.response.send_message("Abgelehnt! DM gesendet. Ticket schließt sich...", ephemeral=True)
        await asyncio.sleep(2)
        try:
            await interaction.channel.delete()
        except:
            pass

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

token = os.getenv("TOKEN")
if token:
    bot.run(token)
else:
    print("FEHLER: Kein Token gefunden!")
