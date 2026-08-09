import os
import threading
import discord
from discord.ext import commands, tasks
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# Globale Variablen für den Bot-Status
bot_ping_ms = 0
bot_status_text = "Offline"

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Phantom Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            margin: 0;
            display: flex;
            flex-direction: column;
            height: 100vh;
            width: 100vw;
            overflow-x: hidden;
        }
        /* Feste obere Leiste */
        .top-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background-color: #1e293b;
            display: flex;
            align-items: center;
            padding: 0 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            z-index: 102;
            box-sizing: border-box;
        }
        .menu-btn {
            background: none;
            border: none;
            color: #f8fafc;
            font-size: 24px;
            cursor: pointer;
            margin-right: 15px;
            padding: 0;
        }
        .app-title {
            color: #38bdf8;
            font-size: 18px;
            font-weight: bold;
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
            top: 60px;
            height: calc(100vh - 60px);
            left: -250px;
            transition: left 0.3s ease;
            z-index: 101;
            box-sizing: border-box;
        }
        .sidebar.open {
            left: 0;
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
            margin-top: 60px;
            height: calc(100vh - 60px);
            width: 100vw;
            padding: 20px;
            box-sizing: border-box;
        }
        .card {
            background-color: #1e293b;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 320px;
            width: 90%;
        }
        h1 { color: #38bdf8; margin-bottom: 5px; font-size: 22px; }
        p { color: #94a3b8; font-size: 14px; margin-bottom: 20px; }
        .info-box {
            background-color: #0f172a;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 14px;
            color: #94a3b8;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .ping-value {
            color: #38bdf8;
            font-weight: bold;
        }
        .status {
            display: inline-block;
            background-color: #ef4444;
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <!-- Feste obere Leiste -->
    <div class="top-bar">
        <button class="menu-btn" onclick="toggleSidebar()">☰</button>
        <span class="app-title">Phantom Dashboard</span>
    </div>

    <!-- Seitenleiste -->
    <div class="sidebar" id="sidebar">
        <a href="#">🏠 Übersicht</a>
        <a href="#">🤖 Bot Status</a>
        <a href="#">⚙️ Einstellungen</a>
    </div>

    <!-- Hauptbereich -->
    <div class="main-content">
        <div class="card">
            <h1>Phantom Bot</h1>
            <p>Live-Überwachung</p>
            
            <div class="info-box">
                <span>Bot Latenz (Ping):</span>
                <span id="ping" class="ping-value">Lade...</span>
            </div>

            <div id="status-badge" class="status">● Offline</div>
        </div>
    </div>

    <script>
        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('open');
        }

        // Live-Daten alle 3 Sekunden von FastAPI abrufen
        async function updateStatus() {
            try {
                let response = await fetch('/api/status');
                let data = await response.json();
                
                const badge = document.getElementById('status-badge');
                const pingEl = document.getElementById('ping');

                if (data.status === "Online") {
                    badge.innerText = "● Online";
                    badge.style.backgroundColor = "#22c55e";
                    pingEl.innerText = data.ping + " ms";
                } else {
                    badge.innerText = "● Offline";
                    badge.style.backgroundColor = "#ef4444";
                    pingEl.innerText = "-";
                }
            } catch (err) {
                console.error("Fehler beim Abrufen des Status");
            }
        }

        setInterval(updateStatus, 3000);
        updateStatus();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_CONTENT

@app.get("/api/status")
def api_status():
    return {"status": bot_status_text, "ping": bot_ping_ms}

def run_server():
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

# Discord Bot Setup
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

@tasks.loop(seconds=3)
async def status_loop():
    global bot_ping_ms, bot_status_text
    if bot.is_ready():
        bot_ping_ms = round(bot.latency * 1000)
        bot_status_text = "Online"
    else:
        bot_status_text = "Offline"

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user}')
    if not status_loop.is_running():
        status_loop.start()

if __name__ == "__main__":
    t = threading.Thread(target=run_server)
    t.start()
    TOKEN = os.environ.get('DISCORD_TOKEN')
    if TOKEN:
        bot.run(TOKEN)
