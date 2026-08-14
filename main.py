import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import asyncio
import os

# ==================== EINSTELLUNGEN ====================
OWNER_ID = 1537902770034577522            # <-- HIER DEINE DISCORD ID EINTRAGEN!
ROLLE_1_ID = 1537902471177838592                           # ID der Rolle beim Annehmen (oder 0 lassen)
ROLLE_2_ID = 1537853690076200980                           # Zweite Rolle (optional, sonst 0)
# =======================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Modal für das Bewerbungsformular
class BewerbungsModal(Modal, title="Bewerbungsformular"):
    frage1 = TextInput(
        label="1. Wie alt bist du?",
        style=discord.TextStyle.short,
        placeholder="Dein Alter...",
        required=True,
        max_length=3
    )
    frage2 = TextInput(
        label="2. Warum möchtest du dich bewerben?",
        style=discord.TextStyle.paragraph,
        placeholder="Schreibe hier deine Motivation...",
        required=True,
        max_length=1000
    )
    frage3 = TextInput(
        label="3. Was sind deine Stärken?",
        style=discord.TextStyle.paragraph,
        placeholder="Deine Stärken...",
        required=True,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Deine Bewerbung wird verarbeitet und dein privates Ticket wird erstellt...", ephemeral=True)
        
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Bewerbungen")
        if not category:
            category = await guild.create_category("Bewerbungen")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"bewerbung-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title=f"Neue Bewerbung von {interaction.user.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="1. Alter", value=self.frage1.value, inline=False)
        embed.add_field(name="2. Motivation", value=self.frage2.value, inline=False)
        embed.add_field(name="3. Stärken", value=self.frage3.value, inline=False)

        view = TicketActionView(interaction.user.id)
        await channel.send(content=f"{interaction.user.mention} hat sich beworben!", embed=embed, view=view)


# Buttons für Annehmen und Ablehnen im Ticket
class TicketActionView(View):
    def __init__(self, target_user_id: int):
        super().__init__(timeout=None)
        self.target_user_id = target_user_id

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.green, emoji="✅")
    async def accept_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("Nur der Inhaber darf das tun!", ephemeral=True)
            return

        guild = interaction.guild
        member = guild.get_member(self.target_user_id)
        channel = interaction.channel

        if member:
            try:
                if ROLLE_1_ID != 0:
                    role1 = guild.get_role(ROLLE_1_ID)
                    if role1: await member.add_roles(role1)
                if ROLLE_2_ID != 0:
                    role2 = guild.get_role(ROLLE_2_ID)
                    if role2: await member.add_roles(role2)
            except Exception as e:
                print(f"Rollen-Fehler: {e}")

            try:
                await member.send("🎉 Herzlichen Glückwunsch! Deine Bewerbung wurde **angenommen**.")
            except:
                pass

        await interaction.response.send_message("Bewerbung wurde **angenommen**. Ticket wird geschlossen...", ephemeral=True)
        await asyncio.sleep(3)
        await channel.delete()

    @discord.ui.button(label="Ablehnen", style=discord.ButtonStyle.red, emoji="❌")
    async def deny_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("Nur der Inhaber darf das tun!", ephemeral=True)
            return

        guild = interaction.guild
        member = guild.get_member(self.target_user_id)
        channel = interaction.channel

        if member:
            try:
                await member.send("❌ Leider wurde deine Bewerbung **abgelehnt**.")
            except:
                pass

        await interaction.response.send_message("Bewerbung wurde **abgelehnt**. Ticket wird geschlossen...", ephemeral=True)
        await asyncio.sleep(3)
        await channel.delete()


# Button der das Formular öffnet
class BewerungsStartView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Bewerbung abschicken", style=discord.ButtonStyle.blurple, custom_id="open_bewerbung_modal")
    async def open_modal(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(BewerbungsModal())


@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user.name}")
    bot.add_view(BewerungsStartView())


# Befehl um das Panel in einen Kanal zu senden: /ticket
@bot.tree.command(name="ticket", description="Sendet das Bewerbungs-Panel in diesen Kanal")
@commands.has_permissions(administrator=True)
async def ticket(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📝 Bewirb dich jetzt!",
        description="Klicke auf den Button unten, um das Bewerbungsformular auszufüllen.",
        color=discord.Color.green()
    )
    await interaction.channel.send(embed=embed, view=BewerungsStartView())
    await interaction.response.send_message("Bewerbungs-Panel erfolgreich gesendet!", ephemeral=True)


# Bot über die Render-Umgebungsvariable starten
token = os.getenv("TOKEN")
if not token:
    print("FEHLER: Kein Token gefunden!")
else:
    bot.run(token)
