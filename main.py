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
                font-family: Arial, sans-serif;
                background-color: #0d1117;
                color: #c9d1d9;
                text-align: center;
                padding-top: 50px;
                margin: 0;
            }
            .container {
                max-width: 600px;
                margin: auto;
                background: #161b22;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            }
            h1 {
                color: #58a6ff;
            }
            p {
                font-size: 16px;
                color: #8b949e;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Phantom Dashboard</h1>
            <p>Dein Dashboard ist erfolgreich online und voll funktionsfähig!</p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
