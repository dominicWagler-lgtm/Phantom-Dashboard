import os
import requests
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

bot_settings = {
    "prefix": "/",
    "default_role": "@Student",
    "log_channel": "#bot-logs"
}

# Speichert zugewiesene Rollen pro Server-ID
server_roles = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        
        # Einstellungen speichern
        if action == "save_settings":
            bot_settings["prefix"] = request.form.get("prefix", "/")
            bot_settings["default_role"] = request.form.get("default_role", "@Student")
            bot_settings["log_channel"] = request.form.get("log_channel", "#bot-logs")
            return redirect(url_for("index"))
            
        # Bot von Server kicken
        elif action == "kick_bot":
            guild_id = request.form.get("guild_id")
            bot_token = os.environ.get("DISCORD_TOKEN")
            if bot_token and guild_id:
                headers = {"Authorization": f"Bot {bot_token}"}
                requests.delete(f"https://discord.com/api/v10/users/@me/guilds/{guild_id}", headers=headers)
            return redirect(url_for("index"))

        # Rolle direkt über das Dashboard vergeben
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
        response = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
        if response.status_code == 200:
            servers = response.json()

    html_content = """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>University Bot - Admin Panel</title>
        <style>
            :root {
                --bg-main: #0b0f19;
                --bg-sidebar: #111827;
                --bg-card: #161e2e;
                --border-color: #1f2937;
                --text-main: #f9fafb;
                --text-muted: #9ca3af;
                --accent: #6366f1;
                --accent-hover: #4f46e5;
                --success: #10b981;
                --danger: #ef4444;
                --danger-hover: #dc2626;
                --warning: #f59e0b;
            }
            body {
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
                background-color: var(--bg-main);
                color: var(--text-main);
                margin: 0;
                display: flex;
                min-height: 100vh;
            }
            sidebar {
                width: 260px;
                background-color: var(--bg-sidebar);
                border-right: 1px solid var(--border-color);
                display: flex;
                flex-direction: column;
                padding: 20px;
                box-sizing: border-box;
                transition: transform 0.3s ease;
            }
            body.sidebar-closed sidebar {
                display: none;
            }
            .sidebar-brand {
                font-size: 18px;
                font-weight: bold;
                color: var(--text-main);
                margin-bottom: 30px;
            }
            .nav-menu {
                list-style: none;
                padding: 0;
                margin: 0;
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .nav-item a {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px 16px;
                color: var(--text-muted);
                text-decoration: none;
                border-radius: 10px;
                font-weight: 500;
                font-size: 14px;
                transition: 0.2s;
            }
            .nav-item a:hover, .nav-item.active a {
                background-color: var(--accent);
                color: white;
            }
            .main-content {
                flex: 1;
                padding: 30px;
                overflow-y: auto;
                box-sizing: border-box;
            }
            .header-top {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: var(--bg-card);
                border: 1px solid var(--border-color);
                padding: 20px 30px;
                border-radius: 16px;
                margin-bottom: 30px;
            }
            .header-left {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .toggle-btn {
                background: #1f2937;
                border: 1px solid #374151;
                color: white;
                padding: 8px 12px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }
            h1 { margin: 0; font-size: 20px; }
            .badge {
                background: rgba(16, 185, 129, 0.1);
                color: var(--success);
                padding: 6px 14px;
                border-radius: 50px;
                font-size: 13px;
                font-weight: 600;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }
            .panel {
                background-color: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 24px;
                margin-bottom: 25px;
            }
            .panel h2 {
                margin-top: 0;
                font-size: 18px;
                border-bottom: 1px solid var(--border-color);
                padding-bottom: 15px;
                margin-bottom: 20px;
            }
            /* Kompakte Server Grid */
            .server-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 12px;
            }
            .server-card {
                background: #1f2937;
                border: 1px solid #374151;
                padding: 12px;
                border-radius: 10px;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .server-header {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .server-icon {
                width: 35px;
                height: 35px;
                background: var(--accent);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 14px;
                overflow: hidden;
                flex-shrink: 0;
            }
            .server-icon img { width: 100%; height: 100%; object-fit: cover; }
            .server-info h4 { margin: 0 0 2px 0; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            .server-info p { margin: 0; font-size: 11px; color: var(--text-muted); }
            
            .role-form {
                display: flex;
                gap: 5px;
            }
            .role-input {
                flex: 1;
                background: #111827;
                border: 1px solid #374151;
                color: var(--text-main);
                padding: 6px 8px;
                border-radius: 6px;
                font-size: 12px;
            }
            .server-actions {
                display: flex;
                gap: 6px;
            }
            .btn-action {
                flex: 1;
                padding: 6px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                text-align: center;
                text-decoration: none;
                cursor: pointer;
                border: none;
            }
            .btn-join { background-color: var(--accent); color: white; }
            .btn-join:hover { background-color: var(--accent-hover); }
            .btn-kick { background-color: var(--danger); color: white; }
            .btn-kick:hover { background-color: var(--danger-hover); }
            .btn-role { background-color: #374151; color: white; }
            .btn-role:hover { background-color: #4b5563; }

            .form-group { margin-bottom: 15px; }
            .form-group label { display: block; font-size: 13px; color: var(--text-muted); margin-bottom: 6px; }
            .form-input {
                width: 100%;
                background: #1f2937;
                border: 1px solid #374151;
                color: var(--text-main);
                padding: 10px 14px;
                border-radius: 8px;
                box-sizing: border-box;
                font-size: 14px;
            }
            .btn {
                background-color: var(--accent);
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            }
            .btn:hover { background-color: var(--accent-hover); }
            .alert {
                background: rgba(245, 158, 11, 0.1);
                border: 1px solid rgba(245, 158, 11, 0.3);
                color: var(--warning);
                padding: 15px;
                border-radius: 10px;
                font-size: 14px;
            }
        </style>
    </head>
    <body id="body">

        <sidebar>
            <div class="sidebar-brand">🤖 University Bot</div>
            <ul class="nav-menu">
                <li class="nav-item active"><a href="#">📊 Server & Rollen</a></li>
                <li class="nav-item"><a href="#settings">⚙️ Einstellungen</a></li>
            </ul>
        </sidebar>

        <div class="main-content">
            <div class="header-top">
                <div class="header-left">
                    <button class="toggle-btn" onclick="toggleSidebar()">☰</button>
                    <div>
                        <h1>Admin Dashboard</h1>
                        <p style="margin: 4px 0 0 0; color: var(--text-muted); font-size: 13px;">Kompakte Server-Verwaltung</p>
                    </div>
                </div>
                <div class="badge">Live Verbunden</div>
            </div>

            <!-- Kompakte Live-Server Sektion mit Rollen-Vergabe -->
            <div class="panel">
                <h2>Deine Live-Server</h2>
                {% if servers %}
                    <div class="server-grid">
                        {% for server in servers %}
                            <div class="server-card">
                                <div class="server-header">
                                    <div class="server-icon">
                                        {% if server.icon %}
                                            <img src="https://cdn.discordapp.com/icons/{{ server.id }}/{{ server.icon }}.png" alt="Icon">
                                        {% else %}
                                            {{ server.name[0] }}
                                        {% endif %}
                                    </div>
                                    <div class="server-info" style="min-width: 0;">
                                        <h4 title="{{ server.name }}">{{ server.name }}</h4>
                                        <p>Rolle: <strong>{{ server_roles.get(server.id, 'Keine') }}</strong></p>
                                    </div>
                                </div>
                                
                                <!-- Rollen direkt zuweisen -->
                                <form method="POST" class="role-form">
                                    <input type="hidden" name="action" value="assign_role">
                                    <input type="hidden" name="guild_id" value="{{ server.id }}">
                                    <input type="text" name="role_name" class="role-input" placeholder="Rollenname..." required>
                                    <button type="submit" class="btn-action btn-role">Setzen</button>
                                </form>

                                <div class="server-actions">
                                    <a href="https://discord.com/channels/{{ server.id }}" target="_blank" class="btn-action btn-join">Join</a>
                                    <form method="POST" style="flex: 1; display: flex;" onsubmit="return confirm('Bot wirklich kicken?');">
                                        <input type="hidden" name="action" value="kick_bot">
                                        <input type="hidden" name="guild_id" value="{{ server.id }}">
                                        <button type="submit" class="btn-action btn-kick" style="width: 100%;">Löschen</button>
                                    </form>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <div class="alert">
                        <strong>Kein Bot-Token hinterlegt!</strong> Füge in Railway unter <strong>Variables</strong> die Variable <code>DISCORD_TOKEN</code> hinzu.
                    </div>
                {% endif %}
            </div>

            <!-- Einstellungen -->
            <div class="panel" id="settings">
                <h2>Allgemeine Einstellungen</h2>
                <form method="POST">
                    <input type="hidden" name="action" value="save_settings">
                    <div class="form-group">
                        <label>Bot-Präfix</label>
                        <input type="text" class="form-input" name="prefix" value="{{ settings.prefix }}">
                    </div>
                    <div class="form-group">
                        <label>Standard-Rolle</label>
                        <input type="text" class="form-input" name="default_role" value="{{ settings.default_role }}">
                    </div>
                    <div class="form-group">
                        <label>Log-Channel</label>
                        <input type="text" class="form-input" name="log_channel" value="{{ settings.log_channel }}">
                    </div>
                    <button type="submit" class="btn">Speichern</button>
                </form>
            </div>
        </div>

        <script>
            function toggleSidebar() {
                document.getElementById('body').classList.toggle('sidebar-closed');
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content, servers=servers, settings=bot_settings, server_roles=server_roles)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
