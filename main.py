import os
import requests
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    # Versuche, echte Server über den Discord Bot Token zu laden, falls hinterlegt
    bot_token = os.environ.get("DISCORD_TOKEN")
    servers = []
    
    if bot_token:
        headers = {
            "Authorization": f"Bot {bot_token}"
        }
        response = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
        if response.status_code == 200:
            servers = response.json()

    # HTML Template für das Admin-Dashboard
    html_content = """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>University Bot - Admin Dashboard</title>
        <style>
            :root {
                --bg-main: #0b0f19;
                --bg-card: #111827;
                --border-color: #1f2937;
                --text-main: #f9fafb;
                --text-muted: #9ca3af;
                --accent: #6366f1;
                --success: #10b981;
                --warning: #f59e0b;
            }
            body {
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
                background-color: var(--bg-main);
                color: var(--text-main);
                margin: 0;
                padding: 30px;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: var(--bg-card);
                border: 1px solid var(--border-color);
                padding: 20px 30px;
                border-radius: 16px;
                margin-bottom: 30px;
            }
            h1 { margin: 0; font-size: 22px; }
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
            .server-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
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
        <div class="container">
            <header>
                <div>
                    <h1>University Bot Admin Panel</h1>
                    <p style="margin: 4px 0 0 0; color: var(--text-muted); font-size: 13px;">Echtzeit Server-Verwaltung</p>
                </div>
                <div class="badge">Live API Verbunden</div>
            </header>

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
                        <strong>Kein Bot-Token gefunden oder keine Server verfügbar!</strong> 
                        Damit hier deine echten Server angezeigt werden, musst du in Railway unter <strong>Variables</strong> die Variable <code>DISCORD_TOKEN</code> mit dem echten Token deines Discord-Bots hinterlegen und den Service neu starten.
                    </div>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content, servers=servers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
