import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phantom Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #121212;
            color: #ffffff;
            margin: 0;
            padding: 0;
        }
        #welcome-screen {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }
        #welcome-screen h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
        }
        .btn {
            background-color: #6200ea;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 1rem;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .btn:hover {
            background-color: #3700b3;
        }
        #dashboard {
            display: none;
            padding: 20px;
        }
    </style>
</head>
<body>

    <!-- Willkommensseite / Vorderseite -->
    <div id="welcome-screen">
        <h1>Willkommen im Phantom Dashboard</h1>
        <button class="btn" onclick="startDashboard()">Starten</button>
    </div>

    <!-- Das eigentliche Dashboard -->
    <div id="dashboard">
        <h1>Phantom Dashboard</h1>
        <p>Du bist erfolgreich auf dem Dashboard angekommen!</p>
    </div>

    <script>
        function startDashboard() {
            document.getElementById('welcome-screen').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
        }
    </script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
