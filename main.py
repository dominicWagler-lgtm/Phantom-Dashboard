import os
import requests
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Bot-Einstellungen
bot_settings = {
    "prefix": "/",
    "default_role": "@Student",
    "log_channel": "#bot-logs"
}

# Lokaler Speicher für zugewiesene Rollen
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
                    error_message = "Fehler beim Entfernen des Bots vom Server."
            return redirect(url_for("index"))

        elif action == "assign_role":
            guild_id = request.form.get("guild_id")
            role_name = request.form.get("role_name")
            if guild_id and role_name:
                server_roles[guild_id] = role_name
            return redirect(url_for("index"))

    # Live-Server via Discord API laden
    bot_token = os.environ.get("DISCORD_TOKEN")
    servers = []
    
    if bot_token:
        headers = {"Authorization": f"Bot {bot_token}"}
        try:
            response = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers, timeout=5)
            if response.status_code == 200:
                servers = response.json()
            else:
                error_message = "Ungültiger Bot-Token oder API-Fehler."
        except Exception:
            error_message = "Verbindung zur Discord-API fehlgeschlagen."

    html_content = """
    <!DOCTYPE html>
    <html lang="de" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>University Bot - Enterprise Dashboard</title>
        <!-- Tailwind CSS CDN -->
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
    <body class="bg-darkBg text-gray-100 font-sans antialiased flex min-h-screen selection:bg-indigo-500 selection:text-white">

        <!-- Sidebar -->
        <aside id="sidebar" class="w-64 bg-cardBg border-r border-cardBorder flex flex-col p-5 transition-all duration-300 z-20">
            <div class="flex items-center gap-3 mb-8 px-2">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center font-bold text-lg shadow-lg shadow-indigo-500/20">
                    🤖
                </div>
                <div>
                    <h2 class="font-bold text-sm tracking-wide">University Bot</h2>
                    <span class="text-xs text-emerald-400 flex items-center gap-1.5 mt-0.5">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Online
                    </span>
                </div>
            </div>

            <nav class="space-y-1 flex-1">
                <a href="#" class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl bg-indigo-600/10 text-indigo-400 font-medium text-sm transition-colors border border-indigo-500/20">
                    📊 Server & Verwaltung
                </a>
                <a href="#settings" class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-gray-400 hover:bg-gray-800/50 hover:text-gray-200 font-medium text-sm transition-colors">
                    ⚙️ Bot-Einstellungen
                </a>
            </nav>

            <div class="pt-4 border-t border-cardBorder text-xs text-gray-500 text-center">
                v2.5 Enterprise Edition
            </div>
        </aside>

        <!-- Hauptinhalt -->
        <main class="flex-1 flex flex-col min-w-0 overflow-y-auto p-6 md:p-10">
            
            <!-- Top Header -->
            <header class="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-cardBg border border-cardBorder p-6 rounded-2xl shadow-xl mb-8 gap-4">
                <div class="flex items-center gap-4">
                    <button onclick="toggleSidebar()" class="p-2.5 rounded-xl bg-gray-800/60 hover:bg-gray-800 border border-cardBorder text-gray-300 transition-colors">
                        ☰
                    </button>
                    <div>
                        <h1 class="text-xl font-bold tracking-tight">Admin Control Center</h1>
                        <p class="text-xs text-gray-400 mt-0.5">Echtzeit-Steuerung deiner Discord-Infrastruktur</p>
                    </div>
                </div>
                <div class="flex items-center gap-3">
                    <div class="px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-emerald-500"></span> API Verbunden
                    </div>
                </div>
            </header>

            {% if error_message %}
            <div class="mb-6 p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 text-sm flex items-center gap-3">
                ⚠️ <span>{{ error_message }}</span>
            </div>
            {% endif %}

            <!-- Statistik-Leiste -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-5 mb-8">
                <div class="bg-cardBg border border-cardBorder p-5 rounded-2xl shadow-lg">
                    <span class="text-xs font-semibold uppercase tracking-wider text-gray-400">Aktive Server</span>
                    <p class="text-2xl font-black mt-2 text-indigo-400">{{ servers|length }}</p>
                </div>
                <div class="bg-cardBg border border-cardBorder p-5 rounded-2xl shadow-lg">
                    <span class="text-xs font-semibold uppercase tracking-wider text-gray-400">System Status</span>
                    <p class="text-2xl font-black mt-2 text-emerald-400">Optimal</p>
                </div>
                <div class="bg-cardBg border border-cardBorder p-5 rounded-2xl shadow-lg">
                    <span class="text-xs font-semibold uppercase tracking-wider text-gray-400">Latenz</span>
                    <p class="text-2xl font-black mt-2 text-purple-400">~14 ms</p>
                </div>
            </div>

            <!-- Server Sektion -->
            <div class="bg-cardBg border border-cardBorder p-6 md:p-8 rounded-2xl shadow-xl mb-8">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-6 border-b border-cardBorder mb-6 gap-4">
                    <div>
                        <h2>Verbundene Discord-Server</h2>
                        <p class="text-xs text-gray-400 mt-0.5">Verwalte Berechtigungen und Zugänge direkt</p>
                    </div>
                    <!-- Live Suchfeld -->
                    <input type="text" id="serverSearch" placeholder="Server suchen..." onkeyup="filterServers()" class="w-full sm:w-64 bg-darkBg border border-cardBorder px-4 py-2 rounded-xl text-sm focus:outline-none focus:border-indigo-500 transition-colors">
                </div>

                {% if servers %}
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5" id="serverGrid">
                        {% for server in servers %}
                            <div class="server-card bg-darkBg border border-cardBorder p-5 rounded-xl flex flex-col justify-between gap-4 hover:border-indigo-500/40 transition-all shadow-md" data-name="{{ server.name | lower }}">
                                <div class="flex items-center gap-3.5">
                                    <div class="w-12 h-12 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center font-bold text-indigo-400 overflow-hidden shrink-0 shadow-inner">
                                        {% if server.icon %}
                                            <img src="https://cdn.discordapp.com/icons/{{ server.id }}/{{ server.icon }}.png" alt="Icon" class="w-full h-full object-cover">
                                        {% else %}
                                            {{ server.name[0] }}
                                        {% endif %}
                                    </div>
                                    <div class="min-w-0 flex-1">
                                        <h4 class="font-bold text-sm truncate" title="{{ server.name }}">{{ server.name }}</h4>
                                        <p class="text-xs text-gray-400 mt-0.5">Rolle: <span class="text-indigo-300 font-medium">{{ server_roles.get(server.id, 'Keine') }}</span></p>
                                    </div>
                                </div>
                                
                                <!-- Rollen-Formular -->
                                <form method="POST" class="flex gap-2">
                                    <input type="hidden" name="action" value="assign_role">
                                    <input type="hidden" name="guild_id" value="{{ server.id }}">
                                    <input type="text" name="role_name" placeholder="Rolle eingeben..." required class="flex-1 bg-cardBg border border-cardBorder px-3 py-1.5 rounded-lg text-xs focus:outline-none focus:border-indigo-500 text-gray-200">
                                    <button type="submit" class="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 border border-cardBorder rounded-lg text-xs font-semibold transition-colors">Setzen</button>
                                </form>

                                <!-- Aktions-Buttons -->
                                <div class="flex gap-2 pt-2 border-t border-cardBorder/60">
                                    <a href="https://discord.com/channels/{{ server.id }}" target="_blank" class="flex-1 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold text-center transition-colors shadow-lg shadow-indigo-600/20">
                                        Beitreten
                                    </a>
                                    <form method="POST" class="flex-1" onsubmit="return confirm('Möchtest du den Bot wirklich von {{ server.name }} entfernen?');">
                                        <input type="hidden" name="action" value="kick_bot">
                                        <input type="hidden" name="guild_id" value="{{ server.id }}">
                                        <button type="submit" class="w-full py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 rounded-lg text-xs font-semibold transition-colors">
                                            Entfernen
                                        </button>
                                    </form>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <div class="p-6 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 text-sm">
                        <strong>Kein Bot-Token aktiv!</strong> Bitte trage in Railway unter <strong>Variables</strong> die Variable <code>DISCORD_TOKEN</code> ein und starte den Dienst neu.
                    </div>
                {% endif %}
            </div>

            <!-- Bot-Einstellungen -->
            <div id="settings" class="bg-cardBg border border-cardBorder p-6 md:p-8 rounded-2xl shadow-xl">
                <div class="pb-6 border-b border-cardBorder mb-6">
                    <h2>Globale Bot-Konfiguration</h2>
                    <p class="text-xs text-gray-400 mt-0.5">Passe das Grundverhalten des Bots an</p>
                </div>
                <form method="POST" class="space-y-5 max-w-xl">
                    <input type="hidden" name="action" value="save_settings">
                    <div>
                        <label class="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Bot-Präfix</label>
                        <input type="text" name="prefix" value="{{ settings.prefix }}" class="w-full bg-darkBg border border-cardBorder px-4 py-2.5 rounded-xl text-sm focus:outline-none focus:border-indigo-500 transition-colors">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Standard-Rolle</label>
                        <input type="text" name="default_role" value="{{ settings.default_role }}" class="w-full bg-darkBg border border-cardBorder px-4 py-2.5 rounded-xl text-sm focus:outline-none focus:border-indigo-500 transition-colors">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">Log-Channel</label>
                        <input type="text" name="log_channel" value="{{ settings.log_channel }}" class="w-full bg-darkBg border border-cardBorder px-4 py-2.5 rounded-xl text-sm focus:outline-none focus:border-indigo-500 transition-colors">
                    </div>
                    <button type="submit" class="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-semibold transition-colors shadow-lg shadow-indigo-600/30">
                        Änderungen speichern
                    </button>
                </form>
            </div>
        </main>

        <script>
            function toggleSidebar() {
                const sidebar = document.getElementById('sidebar');
                sidebar.classList.toggle('hidden');
            }

            function filterServers() {
                let input = document.getElementById('serverSearch').value.toLowerCase();
                let cards = document.getElementsByClassName('server-card');
                
                for (let i = 0; i < cards.length; i++) {
                    let name = cards[i].getAttribute('data-name');
                    if (name.includes(input)) {
                        cards[i].style.display = "";
                    } else {
                        cards[i].style.display = "none";
                    }
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
