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
        <title>Phantom | Dashboard</title>
        <style>
            :root {
                --bg: #09090b;
                --card-bg: #18181b;
                --text: #f4f4f5;
                --accent: #3b82f6;
            }
            body {
                font-family: 'Inter', system-ui, sans-serif;
                background-color: var(--bg);
                color: var(--text);
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .container {
                width: 90%;
                max-width: 800px;
                background: var(--card-bg);
                padding: 40px;
                border-radius: 20px;
                border: 1px solid #27272a;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
            }
            h1 { font-size: 2rem; margin-bottom: 10px; }
            .badge {
                background: rgba(59, 130, 246, 0.1);
                color: var(--accent);
                padding: 5px 12px;
                border-radius: 99px;
                font-size: 0.8rem;
                font-weight: 600;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }
            .stat-card {
                background: #27272a;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #3f3f46;
            }
            .stat-card h3 { color: #a1a1aa; font-size: 0.9rem; margin: 0; }
            .stat-card p { font-size: 1.5rem; font-weight: bold; margin: 10px 0 0 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <span class="badge">LIVE STATUS</span>
            <h1>Phantom Dashboard</h1>
            <p style="color: #a1a1aa;">Willkommen auf deinem hochmodernen Dashboard.</p>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>Uptime</h3>
                    <p>100%</p>
                </div>
                <div class="stat-card">
                    <h3>Server</h3>
                    <p>Active</p>
                </div>
                <div class="stat-card">
                    <h3>Latency</h3>
                    <p>~12ms</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
