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

        /* Willkommensseite / Fragen-Screen */
        #welcome-screen {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
            padding: 20px;
        }
        #welcome-screen h1 {
            font-size: 2.2rem;
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
            margin: 5px;
        }
        .btn:hover {
            background-color: #3700b3;
        }
        .question-box {
            display: none;
            background-color: #1e1e1e;
            padding: 30px;
            border-radius: 10px;
            border: 1px solid #333;
            max-width: 400px;
            width: 100%;
        }
        .question-box h2 {
            font-size: 1.3rem;
            margin-bottom: 20px;
        }

        /* Dashboard (standardmäßig unsichtbar) */
        #dashboard {
            display: none;
            height: 100vh;
        }

        /* Linke Menüleiste (ein-/ausklappbar) */
        .sidebar {
            width: 220px;
            background-color: #1e1e1e;
            height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
            padding-top: 20px;
            border-right: 1px solid #333;
            transition: transform 0.3s ease;
            z-index: 100;
        }
        .sidebar.closed {
            transform: translateX(-220px);
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

        /* Hauptbereich des Dashboards */
        .main-content {
            margin-left: 220px;
            padding: 20px;
            transition: margin-left 0.3s ease;
        }
        .main-content.expanded {
            margin-left: 0;
        }
        .top-bar {
            display: flex;
            align-items: center;
            border-bottom: 1px solid #333;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
        .menu-toggle-btn {
            background-color: #333;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 15px;
            font-size: 1rem;
        }
        .menu-toggle-btn:hover {
            background-color: #444;
        }
        .top-header {
            font-size: 1.8rem;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <!-- Vorderseite / Startbildschirm -->
    <div id="welcome-screen">
        <div id="start-btn-container">
            <h1>Willkommen im Phantom Dashboard</h1>
            <button class="btn" onclick="startQuiz()">Starten</button>
        </div>

        <!-- Frage 1 -->
        <div id="q1" class="question-box">
            <h2>Frage 1: Ist der Bot auf eurem Server?</h2>
            <button class="btn" onclick="nextQuestion(1, 'ja')">Ja</button>
            <button class="btn" onclick="nextQuestion(1, 'nein')">Nein</button>
        </div>

        <!-- Frage 2 -->
        <div id="q2" class="question-box">
            <h2>Frage 2: Seid ihr über 10?</h2>
            <button class="btn" onclick="nextQuestion(2, 'ja')">Ja</button>
            <button class="btn" onclick="nextQuestion(2, 'nein')">Nein</button>
        </div>

        <!-- Frage 3 -->
        <div id="q3" class="question-box">
            <h2>Frage 3: Ist der Bot gut?</h2>
            <button class="btn" onclick="nextQuestion(3, 'ja')">Ja</button>
            <button class="btn" onclick="nextQuestion(3, 'nein')">Nein</button>
        </div>
    </div>

    <!-- Das eigentliche Dashboard (erscheint nach den Fragen) -->
    <div id="dashboard">
        <!-- Linke Menüleiste -->
        <div id="sidebar" class="sidebar">
            <h2>Phantom Menu</h2>
            <a href="#">Übersicht</a>
            <a href="#">Einstellungen</a>
            <a href="#">Statistiken</a>
            <a href="#">Logout</a>
        </div>

        <!-- Rechter Hauptbereich -->
        <div id="main-content" class="main-content">
            <div class="top-bar">
                <button class="menu-toggle-btn" onclick="toggleSidebar()">☰ Menü</button>
                <div class="top-header">Phantom Dashboard</div>
            </div>
            <p>Du hast alle Fragen beantwortet und bist erfolgreich auf dem Dashboard angekommen!</p>
        </div>
    </div>

    <script>
        function startQuiz() {
            // Start-Button ausblenden, Frage 1 anzeigen
            document.getElementById('start-btn-container').style.display = 'none';
            document.getElementById('q1').style.display = 'block';
        }

        function nextQuestion(current, answer) {
            // Aktuelle Frage verstecken
            document.getElementById('q' + current).style.display = 'none';

            let next = current + 1;
            if (next <= 3) {
                // Nächste Frage anzeigen
                document.getElementById('q' + next).style.display = 'block';
            } else {
                // Wenn alle Fragen beantwortet sind: Willkommensscreen komplett ausblenden und Dashboard zeigen
                document.getElementById('welcome-screen').style.display = 'none';
                document.getElementById('dashboard').style.display = 'block';
            }
        }

        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const mainContent = document.getElementById('main-content');
            
            sidebar.classList.toggle('closed');
            mainContent.classList.toggle('expanded');
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
