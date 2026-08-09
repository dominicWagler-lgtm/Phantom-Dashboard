import os
import requests
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Globale Variable für Einstellungen (zum Verwalten)
bot_settings = {
    "prefix": "/",
    "default_role": "@Student",
    "log_channel": "#bot-logs"
}

@app.route("/", methods=["GET", "POST"])
def index():
    # Wenn Einstellungen im Admin-Panel geändert und abgesendet werden
    if request.method == "POST":
        bot_settings["prefix"] = request.form.get("prefix", "/")
        bot_settings["default_role"] = request.form.get("default_role", "@Student")
        bot_settings["log_channel"] = request.form.get("log_channel", "#bot-logs")
        return redirect(url_for("index"))

    # Echte Live-Server über den Discord Bot Token laden
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
            /* Sidebar Menüleiste */
            sidebar {
                width: 260px;
                background-color: var(--bg-sidebar);
                border-right: 1px solid var(--border-color);
                display: flex;
                flex-direction: column;
                padding: 20px;
                box-sizing: border-box;
            }
            .sidebar-brand {
                font-size: 18px;
                font-weight: bold;
                color: var(--text-main);
                margin-bottom: 30px;
                display: flex;
                align-items: center;
                gap: 10px;
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
            /* Hauptbereich */
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
            /* Server Grid */
            .server-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 15px;
            }
            .server-card {
                background: #1f2937;
                border: 1px solid #374151;
                padding: 16px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .server-icon {
                width: 45px;
                height: 45px;
                background: var(--accent);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 18px;
                overflow: hidden;
            }
            .server-icon img { width: 100%; height: 100%; object-fit: cover; }
            .server-info h4 { margin: 0 0 4px 0; font-size: 15px; }
            .server-info p { margin: 0; font-size: 12px; color: var(--text-muted); }
            /* Formulare */
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
    <body>

        <!-- Linke Menüleiste (Sidebar) -->
        <sidebar>
            <div class="sidebar-brand">
                🤖 University Bot
            </div>
            <ul class="nav-menu">
                <li class="nav-item active"><a href="#">📊 Übersicht & Server</a></li>
                <li class="nav-item"><a href="#settings">⚙️ Bot-Einstellungen</a></li>
            </ul>
        </sidebar>

        <!-- Rechter Verwaltungsbereich -->
        <div class="main-content">
            <div class="header-top">
                <div>
                    <h1>Admin Dashboard</h1>
                    <p style="margin: 4px 0 0 0; color: var(--text-muted); font-size: 13px;">Echtzeit-Verwaltung</p>
                </div>
                <div class="badge">Live Verbunden</div>
            </div>

            <!-- Live Server Sektion -->
            <div class="panel">
                <h2>Echte Live-Server (Auf denen der Bot ist)</h2>
                {% if servers %}
                    <div class="server-grid">
                        {% for server in servers %}
                            <div class="server-card">
                                <div class="server-icon">
                                    {% if server.icon %}
                                        <img src="https://cdn.discordapp.com/icons/{{ server.id }}/{{ server.icon }}.png" alt="Icon">
                                    {% else %}
                                        {{ server.name[0] }}
                                    {% endif %}
                                </div>
                                <div class="server-info">
                                    <h4>{{ server.name }}</h4>
                                    <p>ID: {{ server.id }}</p>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <div class="alert">
                        <strong>Kein Bot-Token hinterlegt!</strong> Füge in Railway unter <strong>Variables</strong> die Variable <code>DISCORD_TOKEN</code> hinzu, damit deine echten Server hier live geladen werden.
                    </div>
                {% endif %}
            </div>

            <!-- Bot-Einstellungen verwalten Sektion -->
            <div class="panel" id="settings">
                <h2>Bot-Einstellungen verwalten</h2>
                <form method="POST">
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
                    <button type="submit" class="btn">Änderungen speichern</button>
                </form>
            </div>
        </div>

    </body>
    </html>
    """
    return render_template_string(html_content, servers=servers, settings=bot_settings)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
