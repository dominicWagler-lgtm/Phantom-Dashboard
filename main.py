import os
import threading
import discord
from discord.ext import commands
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)
app = FastAPI()

TOKEN = os.environ.get("DISCORD_TOKEN", "DEIN_BOT_TOKEN_HIER_EINSETZEN")
PORT = int(os.environ.get("PORT", 8000))

SCNX_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCNX — University Bot Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-[#0b0f19] text-gray-200 font-sans antialiased">
    <div class="flex h-screen overflow-hidden">
        <aside class="w-64 bg-[#111827] border-r border-gray-800/80 flex flex-col justify-between hidden md:flex">
            <div>
                <div class="flex items-center gap-3 px-6 py-5 border-b border-gray-800/80">
                    <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center text-gray-950 font-black text-lg shadow-lg shadow-emerald-500/20">
                        <i class="fa-solid fa-bolt"></i>
                    </div>
                    <div>
                        <h1 class="font-bold text-base tracking-tight text-white">SCNX</h1>
                        <p class="text-[11px] text-gray-400">University Control</p>
                    </div>
                </div>
                <nav class="p-3 space-y-1">
                    <a href="#" class="flex items-center gap-3 px-4 py-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 font-medium text-sm border border-emerald-500/20 transition">
                        <i class="fa-solid fa-house w-5 text-emerald-400"></i> Dashboard
                    </a>
                </nav>
            </div>
            <div class="p-4 border-t border-gray-800/80 text-xs text-gray-500 flex items-center justify-between">
                <span>Bot Status: Online</span>
                <i class="fa-solid fa-circle text-[8px] text-emerald-500 animate-pulse"></i>
            </div>
        </aside>
        <main class="flex-1 flex flex-col overflow-y-auto">
            <header class="h-16 bg-[#111827]/60 backdrop-blur-md border-b border-gray-800/80 px-6 flex items-center justify-between sticky top-0 z-20">
                <div class="flex items-center gap-3">
                    <span class="text-xs text-gray-400 font-medium">University Dashboard</span>
                    <i class="fa-solid fa-chevron-right text-[10px] text-gray-600"></i>
                    <span class="text-xs text-emerald-400 font-semibold">Live Server Panel</span>
                </div>
            </header>
            <div class="p-8 max-w-7xl mx-auto w-full space-y-6">
                <div class="bg-[#111827] border border-gray-800 rounded-2xl p-6 shadow-sm flex items-center justify-between">
                    <div class="flex items-center gap-5">
                        <div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-700 flex items-center justify-center text-3xl shadow-lg">
                            🤖
                        </div>
                        <div>
                            <h2 class="text-2xl font-bold text-white">Bot Live Control</h2>
                            <p class="text-xs text-emerald-400 mt-1">● Verbunden mit Discord-Gateway | Latenz: {ping} ms</p>
                        </div>
                    </div>
                </div>
                <div class="bg-[#111827] border border-gray-800 rounded-2xl p-6 space-y-4">
                    <div class="flex items-center justify-between">
                        <h3 class="text-lg font-bold text-white">Aktive Server des Bots</h3>
                        <span class="text-xs bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-full border border-emerald-500/20">Live Sync</span>
                    </div>
                    <div class="grid grid-cols-1 gap-3">
                        {guild_list}
                    </div>
                </div>
            </div>
        </main>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def dashboard_home():
    b_ping = round(bot.latency * 1000) if bot.latency else 0
    guilds_html = ""
    if bot.guilds:
        for guild in bot.guilds:
            guilds_html += f"""
            <div class="flex items-center justify-between p-4 bg-[#0b0f19] rounded-xl border border-gray-800">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-white text-sm">
                        {guild.name[:2].upper()}
                    </div>
                    <div>
                        <p class="font-bold text-white text-sm">{guild.name}</p>
                        <p class="text-xs text-gray-400">Mitglieder: {guild.member_count} | ID: {guild.id}</p>
                    </div>
                </div>
                <span class="px-3 py-1 bg-emerald-500/10 text-emerald-400 text-xs rounded-full border border-emerald-500/20 font-medium">Online</span>
            </div>
            """
    else:
        guilds_html = '<p class="text-gray-400 text-sm py-4 text-center">Der Bot ist aktuell auf keinem Server online oder verbindet sich gerade...</p>'

    html = SCNX_HTML_TEMPLATE.replace("{ping}", str(b_ping)).replace("{guild_list}", guilds_html)
    return html

@bot.event
async def on_ready():
    print(f"Bot ist eingeloggt als {bot.user}")

def run_web():
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    bot.run(TOKEN)
