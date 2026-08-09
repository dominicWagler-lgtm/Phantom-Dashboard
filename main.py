import os
import requests
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

bot_settings = {
    "prefix": "/",
    "default_role": "@Student",
    "log_channel": "#bot-logs"
}

server_roles = {}

@app.route("/", methods=["GET", "POST"])
def index():
    error_message = None
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "save_settings":
            bot_settings["prefix"] = request.form.get("prefix", "/")
            bot_settings["default_role"] = request.form.get("default_role", "@Student")
            bot_settings["log_channel"] = request.form.get("log_channel", "#bot-logs")
            return redirect(url_for("index"))
            
        elif action == "kick_bot":
            guild_id = request.form.get("guild_id")
            bot_token = os.environ.get("DISCORD_TOKEN")
            if bot_token and guild_id:
                headers = {"Authorization": f"Bot {bot_token}"}
                res = requests.delete(f"https://discord.com/api/v10/users/@me/guilds/{guild_id}", headers=headers)
                if res.status_code != 204:
                    error_message = "Fehler beim Entfernen des Bots."
            return redirect(url_for("index"))

        elif action == "assign_role":
            guild_id = request.form.get("guild_id")
            role_name = request.form.get("role_name")
            if guild_id and role_name:
                server_roles[guild_id] = role_name
            return redirect(url_for("index"))

    bot_token = os.environ.get("DISCORD_TOKEN")
    servers = []
    
    if bot_token:
        headers = {"Authorization": f"Bot {bot_token}"}
        try:
            response = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers, timeout=5)
            if response.status_code == 200:
                servers = response.json()
            else:
                error_message = "Ungültiger Bot-Token."
        except Exception:
            error_message = "API-Verbindungsfehler."

    html_content = """
    <!DOCTYPE html>
    <html lang="de" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>University Bot - Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {
                darkMode: 'class',
                theme: {
                    extend: {
                        colors: {
                            darkBg: '#090a0f',
                            cardBg: '#121622',
                            cardBorder: '#1e263d',
                            accent: '#6366f1',
                            accentHover: '#4f46e5'
                        }
                    }
                }
            }
        </script>
    </head>
    <body class="bg-darkBg text-gray-100 font-sans antialiased flex flex-col md:flex-row min-h-screen">

        <!-- Sidebar (Mobil ausblackbar, Desktop fest) -->
        <aside id="sidebar" class="fixed md:static inset-y-0 left-0 transform -translate-x-full md:translate-x-0 w-64 bg-cardBg border-r border-cardBorder flex flex-col p-5 transition-transform duration-300 z-50">
            <div class="flex items-center justify-between mb-8 px-2">
                <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center font-bold text-lg shadow-lg">🤖</div>
                    <div>
                        <h2 class="font-bold text-sm">University Bot</h2>
                        <span class="text-xs text-emerald-400 flex items-center gap-1.5 mt-0.5">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Online
                        </span>
                    </div>
                </div>
                <button onclick="toggleSidebar()" class="md:hidden text-gray-400 hover:text-white text-lg">✕</button>
            </div>

            <nav class="space-y-1 flex-1">
                <a href="#" class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl bg-indigo-600/10 text-indigo-400 font-medium text-sm border border-indigo-500/20">
                    📊 Server & Verwaltung
                </a>
                <a href="#settings" class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-gray-400 hover:bg-gray-800/50 hover:text-gray-200 font-medium text-sm">
                    ⚙️ Einstellungen
                </a>
            </nav>
            <div class="pt-4 border-t border-cardBorder text-xs text-gray-500 text-center">v2.6 Mobile Ready</div>
        </aside>

        <!-- Hauptinhalt -->
        <main class="flex-1 flex flex-col min-w-0 p-4 md:p-10 max-w-full">
            
            <header class="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-cardBg border border-cardBorder p-5 rounded-2xl shadow-xl mb-6 gap-4">
                <div class="flex items-center gap-3">
                    <button onclick="toggleSidebar()" class="p-2.5 rounded-xl bg-gray-800 hover:bg-gray-700 border border-cardBorder text-gray-300">
                        ☰
                    </button>
                    <div>
                        <h1 class="text-lg md:text-xl font-bold">Admin Control Center</h1>
                        <p class="text-xs text-gray-400">Echtzeit-Steuerung</p>
                    </div>
                </div>
                <div class="px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Verbunden
                </div>
            </header>

            {% if error_message %}
            <div class="mb-6 p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 text-sm">
                ⚠️ {{ error_message }}
            </div>
            {% endif %}

            <!-- Statistik -->
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-6">
                <div class="bg-cardBg border border-cardBorder p-4 rounded-xl">
                    <span class="text-xs text-gray-400">Server</span>
                    <p class="text-xl font-bold text-indigo-400 mt-1">{{ servers|length }}</p>
                </div>
                <div class="bg-cardBg border border-cardBorder p-4 rounded-xl">
                    <span class="text-xs text-gray-400">Status</span>
                    <p class="text-xl font-bold text-emerald-400 mt-1">Aktiv</p>
                </div>
                <div class="bg-cardBg border border-cardBorder p-4 rounded-xl col-span-2 sm:col-span-1">
                    <span class="text-xs text-gray-400">Ping</span>
                    <p class="text-xl font-bold text-purple-400 mt-1">~14 ms</p>
                </div>
            </div>

            <!-- Server Sektion -->
            <div class="bg-cardBg border border-cardBorder p-5 md:p-6 rounded-2xl shadow-xl mb-6">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-4 border-b border-cardBorder mb-5 gap-3">
                    <h2 class="text-base font-bold">Verbundene Server</h2>
                    <input type="text" id="serverSearch" placeholder="Suchen..." onkeyup="filterServers()" class="w-full sm:w-48 bg-darkBg border border-cardBorder px-3 py-1.5 rounded-xl text-xs focus:outline-none focus:border-indigo-500">
                </div>

                {% if servers %}
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="serverGrid">
                        {% for server in servers %}
                            <div class="server-card bg-darkBg border border-cardBorder p-4 rounded-xl flex flex-col justify-between gap-3 shadow" data-name="{{ server.name | lower }}">
                                <div class="flex items-center gap-3">
                                    <div class="w-10 h-10 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center font-bold text-indigo-400 overflow-hidden shrink-0">
                                        {% if server.icon %}
                                            <img src="https://cdn.discordapp.com/icons/{{ server.id }}/{{ server.icon }}.png" alt="Icon" class="w-full h-full object-cover">
                                        {% else %}
                                            {{ server.name[0] }}
                                        {% endif %}
                                    </div>
                                    <div class="min-w-0 flex-1">
                                        <h4 class="font-bold text-xs truncate" title="{{ server.name }}">{{ server.name }}</h4>
                                        <p class="text-[11px] text-gray-400 mt-0.5">Rolle: <span class="text-indigo-300 font-medium">{{ server_roles.get(server.id, 'Keine') }}</span></p>
                                    </div>
                                </div>
                                
                                <form method="POST" class="flex gap-2">
                                    <input type="hidden" name="action" value="assign_role">
                                    <input type="hidden" name="guild_id" value="{{ server.id }}">
                                    <input type="text" name="role_name" placeholder="Rolle..." required class="flex-1 bg-cardBg border border-cardBorder px-2.5 py-1 rounded-lg text-xs focus:outline-none focus:border-indigo-500 text-gray-200">
                                    <button type="submit" class="px-2.5 py-1 bg-gray-800 hover:bg-gray-700 border border-cardBorder rounded-lg text-xs font-semibold">Setzen</button>
                                </form>

                                <div class="flex gap-2 pt-2 border-t border-cardBorder/60">
                                    <a href="https://discord.com/channels/{{ server.id }}" target="_blank" class="flex-1 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold text-center transition-colors">
                                        Join
                                    </a>
                                    <form method="POST" class="flex-1" onsubmit="return confirm('Bot wirklich löschen?');">
                                        <input type="hidden" name="action" value="kick_bot">
                                        <input type="hidden" name="guild_id" value="{{ server.id }}">
                                        <button type="submit" class="w-full py-1.5 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 rounded-lg text-xs font-semibold transition-colors">
                                            Löschen
                                        </button>
                                    </form>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs">
                        Kein Bot-Token aktiv in Railway (`DISCORD_TOKEN`).
                    </div>
                {% endif %}
            </div>

            <!-- Einstellungen -->
            <div id="settings" class="bg-cardBg border border-cardBorder p-5 md:p-6 rounded-2xl shadow-xl">
                <div class="pb-4 border-b border-cardBorder mb-4">
                    <h2 class="text-base font-bold">Bot-Einstellungen</h2>
                </div>
                <form method="POST" class="space-y-4 max-w-xl">
                    <input type="hidden" name="action" value="save_settings">
                    <div>
                        <label class="block text-xs font-semibold text-gray-400 mb-1">Bot-Präfix</label>
                        <input type="text" name="prefix" value="{{ settings.prefix }}" class="w-full bg-darkBg border border-cardBorder px-3 py-2 rounded-xl text-xs focus:outline-none focus:border-indigo-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-400 mb-1">Standard-Rolle</label>
                        <input type="text" name="default_role" value="{{ settings.default_role }}" class="w-full bg-darkBg border border-cardBorder px-3 py-2 rounded-xl text-xs focus:outline-none focus:border-indigo-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-400 mb-1">Log-Channel</label>
                        <input type="text" name="log_channel" value="{{ settings.log_channel }}" class="w-full bg-darkBg border border-cardBorder px-3 py-2 rounded-xl text-xs focus:outline-none focus:border-indigo-500">
                    </div>
                    <button type="submit" class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold shadow-lg">
                        Speichern
                    </button>
                </form>
            </div>
        </main>

        <script>
            function toggleSidebar() {
                const sidebar = document.getElementById('sidebar');
                sidebar.classList.toggle('-translate-x-full');
            }

            function filterServers() {
                let input = document.getElementById('serverSearch').value.toLowerCase();
                let cards = document.getElementsByClassName('server-card');
                for (let i = 0; i < cards.length; i++) {
                    let name = cards[i].getAttribute('data-name');
                    cards[i].style.display = name.includes(input) ? "" : "none";
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content, servers=servers, settings=bot_settings, server_roles=server_roles, error_message=error_message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
