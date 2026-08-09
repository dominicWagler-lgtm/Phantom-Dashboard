import os
import threading
import discord
from discord.ext import commands
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

# FastAPI-App erstellen
app = FastAPI()

# HTML-Inhalt mit Seitenleiste und Drei-Striche-Menü
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phantom Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            margin: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }
        /* Seitenleiste */
        .sidebar {
            width: 250px;
            background-color: #1e293b;
            display: flex;
            flex-direction: column;
            padding: 20px;
            box-shadow: 4px 0 10px rgba(0, 0, 0, 0.2);
            position: fixed;
            height: 100%;
            left: -250px;
            transition: left 0.3s ease;
            z-index: 100;
        }
        .sidebar.open {
            left: 0;
        }
        .sidebar h2 {
            color: #38bdf8;
            font-size: 20px;
            margin-bottom: 30px;
        }
        .sidebar a {
            color: #94a3b8;
            text-decoration: none;
            padding: 12px 15px;
            border-radius: 8px;
            margin-bottom: 8px;
            transition: 0.2s;
            font-weight: 500;
        }
        .sidebar a:hover {
            background-color: #334155;
            color: #fff;
        }
        /* Hauptbereich */
        .main-content {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            width: 100%;
            padding: 20px;
        }
        /* Menü-Button (Drei Striche) */
        .menu-btn {
            position: absolute;
            top: 20px;
            left: 20px;
            background-color: #1e293b;
            border: none;
            color: #f8fafc;
            font-size: 24px;
            padding: 10px 14px;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            z-index: 101;
        }
        .menu-btn:hover {
            background-color: #334155;
        }
        .card {
            background-color: #1e293b;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 400px;
            width: 100%;
        }
        h1 {
            color: #38bdf8;
            margin-bottom: 10px;
        }
        p {
            color: #94a3b8;
            font-size: 16px;
        }
        .status {
            display: inline-block;
            background-color: #22c55e;
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
</head>
<body>

    <!-- Drei-Striche Menü-Button -->
    <button class="menu-btn" onclick="toggleSidebar()">☰</button>

    <!-- Seitenleiste -->
    <div class="sidebar" id="sidebar">
        <h2>Phantom Menu</h2>
        <a href="#">🏠 Übersicht</a>
        <a href="#">🤖 Bot Status</a>
        <a href="#">⚙️ Einstellungen</a>
        <a href="#">📊 Statistiken</a>
    </div>

    <!-- Hauptbereich -->
    <div class="main-content">
        <div class="card">
            <h1>Phantom Dashboard</h1>
            <p>Dein Discord-Bot und Webserver laufen stabil.</p>
            <div class="status">● Online</div>
        </div>
    </div>

    <script>
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('open');
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_CONTENT

def run_server():
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run_server)
    t.start()

# Discord Bot Setup
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user}')

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.environ.get('DISCORD_TOKEN')
    if TOKEN:
        bot.run(TOKEN)
