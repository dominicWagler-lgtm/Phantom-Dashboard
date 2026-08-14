import os
import discord
from discord import app_commands
from discord.ui import Button, View, Modal, TextInput
import asyncio

# --- HIER BITTE ANPASSEN (NUR ZAHLEN) ---
OWNER_ID = 1537902770034577522     # Deine Discord User-ID
ROLLE_1_ID = 1537902471177838592    # Erste Rolle nach Annahme
ROLLE_2_ID = 1537853690076200980    # Zweite Rolle nach Annahme
TICKET_KATEGORIE_ID = 0            # Kategorie-ID (0 lassen, wenn keine gewünscht)

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Bewerbungs-Formular (Modal)
class ApplicationModal(Modal, title="Bewerbungsformular"):
    age = TextInput(
        label='Wie alt bist du? (z.B. 16 oder älter)',
        style=discord.TextStyle.short,
        required=True
    )
    experience = TextInput(
        label='Welche Erfahrungen hast du?',
        style=discord.TextStyle.paragraph,
        required=True
    )
    why_you = TextInput(
        label='Warum sollten wir dich nehmen?',
        style=discord.TextStyle.paragraph,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Deine Bewerbung wird verarbeitet und dein privates Ticket wird erstellt...", ephemeral=True)

        guild = interaction.guild
        user = interaction.user

        category = guild.get_channel(TICKET_KATEGORIE_ID) if TICKET_KATEGORIE_ID != 0 else None
        owner_member = guild.get_member(OWNER_ID)

        # Berechtigungen: Nur der Bewerber, der Owner und der Bot haben Zugriff
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        }
        if owner_member:
            overwrites[owner_member] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

        # Ticket-Kanal erstellen
        ticket_channel = await guild.create_text_channel(
            name=f"bewerbung-{user.name}",
            category=category,
            overwrites=overwrites
        )

        # Embed mit den Antworten
        embed = discord.Embed(
            title=f"🎫 Neue Bewerbung von {user.name}",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Alter / Angaben", value=self.age.value, inline=False)
        embed.add_field(name="Erfahrungen", value=self.experience.value, inline=False)
        embed.add_field(name="Warum wir?", value=self.why_you.value, inline=False)

        view = TicketActionView(user.id)
        owner_mention = f"<@{OWNER_ID}>" if OWNER_ID else ""
        
        await ticket_channel.send(
            content=f"{owner_mention} Neue Bewerbung eingetroffen!",
            embed=embed,
            view=view
        )

# Ansicht für die Annehmen/Ablehnen-Buttons im Ticket
class TicketActionView(View):
    def __init__(self, target_user_id: int):
        super().__init__(timeout=None)
        self.target_user_id = target_user_id

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.green, emoji="✅")
    async def accept_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("Nur der Server-Inhaber darf das tun!", ephemeral=True)
            return

        guild = interaction.guild
        member = guild.get_member(self.target_user_id)
        channel = interaction.channel

        if member:
            try:
                role1 = guild.get_role(ROLLE_1_ID)
                role2 = guild.get_role(ROLLE_2_ID)
                if role1: await member.add_roles(role1)
                if role2: await member.add_roles(role2)
            except Exception as e:
                print(f"Fehler beim Rollen vergeben: {e}")

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
            await interaction.response.send_message("Nur der Server-Inhaber darf das tun!", ephemeral=True)
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

# Slash Command /ticket
@tree.command(name="ticket", description="Öffnet das Bewerbungs-Ticket-Panel")
async def ticket_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎫 Bewerbungs-Panel",
        description="Klicke auf den Button unten, um das Bewerbungsformular auszufüllen.\n\n*Das Ticket ist nach dem Absenden streng vertraulich und nur für dich und den Owner sichtbar!*",
        color=discord.Color.green()
    )
    
    view = View(timeout=None)
    button = Button(label="Bewerbung abschicken", style=discord.ButtonStyle.primary, emoji="📝", custom_id="open_application_modal")
    
    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_modal(ApplicationModal())
        
    button.callback = button_callback
    view.add_item(button)
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Eingeloggt als {client.user}!")

# Bot über die Render-Umgebungsvariable starten
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
             
