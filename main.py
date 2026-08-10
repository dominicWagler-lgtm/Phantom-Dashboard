import os
import requests
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

bot_settings = {
    "prefix": "/",
    "default_role": "Mitglied",
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
            bot_settings["default_role"] = request.form.get("default_role", "Mitglied")
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
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Bot Control Panel</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @keyframes spin-gradient {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .spinning-border {
                position: relative;
                overflow: hidden;
                border-radius: 0.75rem;
                padding: 1px;
            }
            .spinning-border::before {
                content: '';
                position: absolute;
                inset: -50%;
                background: conic-gradient(from 0deg at 50% 50%, #3b82f6 0deg, #ffffff 90deg, #3b82f6 180deg, #ffffff 270deg, #3b82f6 360deg);
                animation: spin-gradient 3s linear infinite;
                z-index: 0;
            }
            .spinning-inner {
                position: relative;
                background: #000000;
                z-index: 1;
                border-radius: calc(0.75rem - 1px);
            }
        </style>
        <script>
            tailwind.config = {
                darkMode: 'class',
                theme: {
                    extend: {
                        colors: {
                            darkBg: '#0b0f19',
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
    <body class="bg-darkBg text-gray-100 font-sans antialiased min-h-screen flex flex-col overflow-x-hidden">

        <!-- Top-Header mit Hamburger-Menü Button (3 Striche) -->
        <header class="bg-cardBg border-b border-cardBorder px-4 py-3 flex justify-between items-center sticky top-0 z-50 shadow-md">
            <div class="flex items-center gap-3">
                <!-- Hamburger Button (3 Striche) -->
                <button onclick="toggleSidebar()" class="w-9 h-9 rounded-xl bg-darkBg border border-cardBorder flex flex-col justify-center items-center gap-1.5 focus:outline-none hover:border-indigo-500 transition-colors">
                    <span class="w-4 h-0.5 bg-white rounded-full"></span>
                    <span class="w-4 h-0.5 bg-white rounded-full"></span>
                    <span class="w-4 h-0.5 bg-white rounded-full"></span>
                </button>
                <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-xs shadow">🤖</div>
                    <h1 class="font-bold text-sm tracking-wide">Bot Control Panel</h1>
                </div>
            </div>
            <div class="flex items-center gap-2 shrink-0">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span class="text-xs text-emerald-400 font-medium">Online</span>
            </div>
        </header>

        <!-- Overlay für das Menü -->
        <div id="sidebarOverlay" onclick="toggleSidebar()" class="fixed inset-0 bg-black/60 z-50 hidden transition-opacity"></div>

        <!-- Ausklappbares Seiten-Menü (Drawer) -->
        <aside id="sidebar" class="fixed top-0 left-0 bottom-0 w-72 bg-cardBg border-r border-cardBorder z-50 transform -translate-x-full transition-transform duration-300 ease-in-out p-5 flex flex-col justify-between shadow-2xl">
            <div>
                <div class="flex justify-between items-center pb-4 border-b border-cardBorder mb-6">
                    <div class="flex items-center gap-2.5">
                        <div class="w-8 h-8 rounded-xl bg-indigo-600 flex items-center justify-center font-bold text-sm shadow">🤖</div>
                        <h2 class="font-bold text-sm">Navigation</h2>
                    </div>
                    <button onclick="toggleSidebar()" class="text-gray-400 hover:text-white text-lg font-bold px-2 py-1">✕</button>
                </div>

                <!-- Menü-Buttons mit rotierendem Blau-Weiß-Rand und schwarzem Inhalt -->
                <nav class="flex flex-col gap-3">
                    <div class="spinning-border shadow-lg">
                        <a href="#" onclick="toggleSidebar()" class="spinning-inner px-3.5 py-3 flex items-center gap-3 text-xs font-semibold text-white block">
                            📊 Dashboard & Server
                        </a>
                    </div>

                    <div class="spinning-border shadow-lg">
                        <a href="#settings" onclick="toggleSidebar()" class="spinning-inner px-3.5 py-3 flex items-center gap-3 text-xs font-semibold text-white block">
                            ⚙️ Bot-Einstellungen
                        </a>
                    </div>

                    <div class="spinning-border shadow-lg">
                        <a href="#serverSearch" onclick="toggleSidebar()" class="spinning-inner px-3.5 py-3 flex items-center gap-3 text-xs font-semibold text-white block">
                            🔍 Server Suchen
                        </a>
                    </div>
                </nav>
            </div>

            <div class="pt-4 border-t border-cardBorder text-[11px] text-gray-500 text-center">
                v3.2 Fully Ready
            </div>
        </aside>

        <!-- Hauptbereich -->
        <main class="flex-1 p-3 sm:p-6 max-w-4xl mx-auto w-full space-y-5 box-border">

            {% if error_message %}
            <div class="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs">
                ⚠️ {{ error_message }}
            </div>
            {% endif %}

            <div class="grid grid-cols-3 gap-2.5">
                <div class="bg-cardBg border border-cardBorder p-3 rounded-xl text-center">
                    <span class="text-[10px] text-gray-400 uppercase tracking-wider block">Server</span>
                    <p class="text-base sm:text-lg font-bold text-indigo-400 mt-0.5">{{ servers|length }}</p>
                </div>
                <div class="bg-cardBg border border-cardBorder p-3 rounded-xl text-center">
                    <span class="text-[10px] text-gray-400 uppercase tracking-wider block">Status</span>
                    <p class="text-base sm:text-lg font-bold text-emerald-400 mt-0.5">Aktiv</p>
                </div>
                <div class="bg-cardBg border border-cardBorder p-3 rounded-xl text-center">
                    <span class="text-[10px] text-gray-400 uppercase tracking-wider block">Ping</span>
                    <p class="text-base sm:text-lg font-bold text-purple-400 mt-0.5">~14 ms</p>
                </div>
            </div>

            <div class="bg-cardBg border border-cardBorder p-4 sm:p-6 rounded-2xl shadow-xl space-y-4">
                <div class="flex flex-col sm:flex-row justify-between items-stretch sm:items-center pb-3 border-b border-cardBorder gap-2.5">
                    <h2 class="text-sm sm:text-base font-bold">Verbundene Server</h2>
                    <input type="text" id="serverSearch" placeholder="Server suchen..." onkeyup="filterServers()" class="w-full sm:w-52 bg-darkBg border border-cardBorder px-3 py-2 rounded-xl text-xs focus:outline-none focus:border-indigo-500 text-gray-200">
                </div>

                {% if servers %}
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5" id="serverGrid">
                        {% for server in servers %}
                            <div class="server-card bg-darkBg border border-cardBorder p-3.5 rounded-xl flex flex-col justify-between gap-3 shadow-sm" data-name="{{ server.name | lower }}">
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
                                        <p class="text-[11px] text-gray-400 mt-0.5 truncate">Rolle: <span class="text-indigo-300 font-medium">{{ server_roles.get(server.id, 'Keine') }}</span></p>
                                    </div>
                                </div>
                                
                                <form method="POST" class="flex gap-2">
                                    <input type="hidden" name="action" value="assign_role">
                                    <input type="hidden" name="guild_id" value="{{ server.id }}">
                                    <input type="text" name="role_name" placeholder="Rolle..." required class="flex-1 bg-cardBg border border-cardBorder px-3 py-2 rounded-lg text-xs focus:outline-none focus:border-indigo-500 text-gray-200 min-w-0">
                                    <button type="submit" class="px-3 py-2 bg-gray-800 hover:bg-gray-700 border border-cardBorder rounded-lg text-xs font-semibold shrink-0">Setzen</button>
                                </form>

                                <div class="flex gap-2 pt-2 border-t border-cardBorder/60">
                                    <a href="https://discord.com/channels/{{ server.id }}" target="_blank" class="flex-1 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold text-center transition-colors shadow-sm">
                                        Join
                                    </a>
                                    <form method="POST" class="flex-1" onsubmit="return confirm('Bot wirklich löschen?');">
                                        <input type="hidden" name="action" value="kick_bot">
                                        <input type="hidden" name="guild_id" value="{{ server.id }}">
                                        <button type="submit" class="w-full py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 rounded-lg text-xs font-semibold transition-colors">
                                            Löschen
                                        </button>
                                    </form>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <div class="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs">
                        Kein Bot-Token aktiv in Railway (`DISCORD_TOKEN`).
                    </div>
                {% endif %}
            </div>

            <div id="settings" class="bg-cardBg border border-cardBorder p-4 sm:p-6 rounded-2xl shadow-xl">
                <div class="pb-3 border-b border-cardBorder mb-4">
                    <h2 class="text-sm sm:text-base font-bold">Bot-Einstellungen</h2>
                </div>
                <form method="POST" class="space-y-3.5">
                    <input type="hidden" name="action" value="save_settings">
                    <div>
                        <label class="block text-xs font-semibold text-gray-400 mb-1">Bot-Präfix</label>
                        <input type="text" name="prefix" value="{{ settings.prefix }}" class="w-full bg-darkBg border border-cardBorder px-3 py-2.5 rounded-xl text-xs focus:outline-none focus:border-indigo-500 text-gray-200">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-400 mb-1">Standard-Rolle</label>
                        <input type="text" name="default_role" value="{{ settings.default_role }}" class="w-full bg-darkBg border border-cardBorder px-3 py-2.5 rounded-xl text-xs focus:outline-none focus:border-indigo-500 text-gray-200">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-400 mb-1">Log-Channel</label>
                        <input type="text" name="log_channel" value="{{ settings.log_channel }}" class="w-full bg-darkBg border border-cardBorder px-3 py-2.5 rounded-xl text-xs focus:outline-none focus:border-indigo-500 text-gray-200">
                    </div>
                    <button type="submit" class="w-full sm:w-auto px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold shadow-lg transition-colors">
                        Speichern
                    </button>
                </form>
            </div>
        </main>

        <script>
            function toggleSidebar() {
                const sidebar = document.getElementById('sidebar');
                const overlay = document.getElementById('sidebarOverlay');
                if (sidebar.classList.contains('-translate-x-full')) {
                    sidebar.classList.remove('-translate-x-full');
                    overlay.classList.remove('hidden');
                } else {
                    sidebar.classList.add('-translate-x-full');
                    overlay.classList.add('hidden');
                }
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
