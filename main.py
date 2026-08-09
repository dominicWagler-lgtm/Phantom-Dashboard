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
        /* Willkommensseite / Vorderseite */
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

        /* Dashboard (standardmäßig unsichtbar) */
        #dashboard {
            display: none;
            height: 100vh;
        }

        /* Linke Menüleiste */
        .sidebar {
            width: 220px;
            background-color: #1e1e1e;
            height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
            padding-top: 20px;
            border-right: 1px solid #333;
        }
        .sidebar h2 {
            color: #b388ff;
            text-align: center;
            font-size: 1.2rem;
            margin-bottom: 30px;
        }
        .sidebar a {
            display: block;
            color: #ffffff;
            text-decoration: none;
            padding: 12px 20px;
            transition: background 0.2s;
        }
        .sidebar a:hover {
            background-color: #333333;
        }

        /* Hauptbereich des Dashboards mit oberem Titel */
        .main-content {
            margin-left: 220px;
            padding: 20px;
        }
        .top-header {
            font-size: 1.8rem;
            font-weight: bold;
            border-bottom: 1px solid #333;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>

    <!-- Vorderseite / Willkommensbildschirm -->
    <div id="welcome-screen">
        <h1>Willkommen im Phantom Dashboard</h1>
        <button class="btn" onclick="startDashboard()">Starten</button>
    </div>

    <!-- Das eigentliche Dashboard (erscheint nach Klick) -->
    <div id="dashboard">
        <!-- Linke Menüleiste -->
        <div class="sidebar">
            <h2>Phantom Menu</h2>
            <a href="#">Übersicht</a>
            <a href="#">Einstellungen</a>
            <a href="#">Statistiken</a>
            <a href="#">Logout</a>
        </div>

        <!-- Rechter Hauptbereich -->
        <div class="main-content">
            <div class="top-header">Phantom Dashboard</div>
            <p>Du bist erfolgreich auf dem Dashboard angekommen!</p>
        </div>
    </div>

    <script>
        function startDashboard() {
            // Versteckt den Willkommensbildschirm
            document.getElementById('welcome-screen').style.display = 'none';
            // Zeigt das Dashboard an
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
