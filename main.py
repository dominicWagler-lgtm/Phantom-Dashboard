import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>University Bot Dashboard</title>
        <style>
            :root {
                --bg-main: #0b0f19;
                --bg-card: #111827;
                --border-color: #1f2937;
                --text-main: #f9fafb;
                --text-muted: #9ca3af;
                --accent: #6366f1;
                --accent-hover: #4f46e5;
                --success: #10b981;
            }
            body {
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
                background-color: var(--bg-main);
                color: var(--text-main);
                margin: 0;
                padding: 30px;
            }
            .dashboard-container {
                max-width: 1200px;
                margin: 0 auto;
            }
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
            .bot-info {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .bot-avatar {
                width: 50px;
                height: 50px;
                background: linear-gradient(135deg, var(--accent), #a855f7);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                font-weight: bold;
            }
            .bot-title h1 {
                margin: 0;
                font-size: 20px;
            }
            .bot-title p {
                margin: 4px 0 0 0;
                font-size: 13px;
                color: var(--text-muted);
            }
            .status-badge {
                display: flex;
                align-items: center;
                gap: 8px;
                background: rgba(16, 185, 129, 0.1);
                color: var(--success);
                padding: 8px 16px;
                border-radius: 50px;
                font-size: 13px;
                font-weight: 600;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }
            .status-dot {
                width: 8px;
                height: 8px;
                background-color: var(--success);
                border-radius: 50%;
                box-shadow: 0 0 8px var(--success);
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background-color: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 24px;
            }
            .stat-card h3 {
                margin: 0 0 8px 0;
                font-size: 13px;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .stat-card .value {
                font-size: 28px;
                font-weight: bold;
                margin: 0;
            }
            .content-grid {
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 25px;
            }
            @media(max-width: 900px) {
                .content-grid {
                    grid-template-columns: 1fr;
                }
            }
            .panel {
                background-color: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                padding: 24px;
            }
            .panel h2 {
                margin-top: 0;
                font-size: 18px;
                border-bottom: 1px solid var(--border-color);
                padding-bottom: 15px;
                margin-bottom: 20px;
            }
            .command-list {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            .command-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: #1f2937;
                padding: 12px 16px;
                border-radius: 10px;
                border: 1px solid #374151;
            }
            .command-name {
                font-family: monospace;
                color: #818cf8;
                font-weight: bold;
            }
            .command-desc {
                font-size: 13px;
                color: var(--text-muted);
            }
            .settings-group {
                margin-bottom: 15px;
            }
            .settings-group label {
                display: block;
                font-size: 13px;
                color: var(--text-muted);
                margin-bottom: 6px;
            }
            .settings-input {
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
                width: 100%;
                padding: 12px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
                margin-top: 10px;
            }
            .btn:hover {
                background-color: var(--accent-hover);
            }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <header>
                <div class="bot-info">
                    <div class="bot-avatar">🤖</div>
                    <div class="bot-title">
                        <h1>University Bot</h1>
                        <p>Dein universitärer Assistent</p>
                    </div>
                </div>
                <div class="status-badge">
                    <span class="status-dot"></span> Online & Verbunden
                </div>
            </header>

            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Aktive Server</h3>
                    <p class="value">42</p>
                </div>
                <div class="stat-card">
                    <h3>Gecachte Nutzer</h3>
                    <p class="value">1,337</p>
                </div>
                <div class="stat-card">
                    <h3>Latenz (Ping)</h3>
                    <p class="value" style="color: #818cf8;">18 ms</p>
                </div>
            </div>

            <div class="content-grid">
                <div class="panel">
                    <h2>Verfügbare Bot-Befehle</h2>
                    <div class="command-list">
                        <div class="command-item">
                            <div>
                                <div class="command-name">/studium plan</div>
                                <div class="command-desc">Zeigt den aktuellen Vorlesungsplan an</div>
                            </div>
                            <span style="color: var(--success); font-size: 12px;">Aktiv</span>
                        </div>
                        <div class="command-item">
                            <div>
                                <div class="command-name">/noten übersicht</div>
                                <div class="command-desc">Gibt die eingetragenen ECTS und Noten aus</div>
                            </div>
                            <span style="color: var(--success); font-size: 12px;">Aktiv</span>
                        </div>
                        <div class="command-item">
                            <div>
                                <div class="command-name">/termin reminder</div>
                                <div class="command-desc">Verwaltet wichtige Fristen und Klausuren</div>
                            </div>
                            <span style="color: var(--success); font-size: 12px;">Aktiv</span>
                        </div>
                    </div>
                </div>

                <div class="panel">
                    <h2>Bot-Einstellungen</h2>
                    <div class="settings-group">
                        <label>Bot-Präfix</label>
                        <input type="text" class="settings-input" value="/" readonly>
                    </div>
                    <div class="settings-group">
                        <label>Standard-Rolle</label>
                        <input type="text" class="settings-input" value="@Student" readonly>
                    </div>
                    <div class="settings-group">
                        <label>Log-Channel</label>
                        <input type="text" class="settings-input" value="#bot-logs" readonly>
                    </div>
                    <button class="btn">Einstellungen speichern</button>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
