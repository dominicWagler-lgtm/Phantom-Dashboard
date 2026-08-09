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
        <title>Phantom Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #0d1117;
                color: #c9d1d9;
                margin: 0;
                padding: 40px;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .dashboard {
                width: 100%;
                max-width: 800px;
                background: #161b22;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.6);
                border: 1px solid #30363d;
            }
            h1 {
                color: #58a6ff;
                margin-top: 0;
                font-size: 28px;
                border-bottom: 1px solid #30363d;
                padding-bottom: 15px;
            }
            .card-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-top: 25px;
            }
            .card {
                background: #21262d;
                padding: 20px;
                border-radius: 8px;
                border: 1px solid #30363d;
            }
            .card h3 {
                margin-top: 0;
                color: #8b949e;
                font-size: 14px;
                text-transform: uppercase;
            }
            .card p {
                font-size: 22px;
                font-weight: bold;
                color: #f0f6fc;
                margin: 10px 0 0 0;
            }
            .status {
                display: inline-block;
                width: 10px;
                height: 10px;
                background-color: #238636;
                border-radius: 50%;
                margin-right: 8px;
            }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <h1>Phantom Dashboard</h1>
            <p><span class="status"></span>Systemstatus: <strong>Online & Stabil</strong></p>
            
            <div class="card-grid">
                <div class="card">
                    <h3>Server</h3>
                    <p>Railway (Nixpacks)</p>
                </div>
                <div class="card">
                    <h3>Modus</h3>
                    <p>Öffentlich (Kein Login)</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
