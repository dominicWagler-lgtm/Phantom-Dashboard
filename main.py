import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Phantom Dashboard</title>
    <style>
        /* Dunkelblaues Design & Verhindern von manuellem horizonthalen Ziehen */
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow-x: hidden;
            background-color: #0a192f;
            color: #ffffff;
            font-family: Arial, sans-serif;
            box-sizing: border-box;
        }

        *, *:before, *:after {
            box-sizing: inherit;
        }

        /* Willkommensseite / Fragen-Screen */
        #welcome-screen {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100vw;
            text-align: center;
            padding: 20px;
            position: absolute;
            top: 0;
            left: 0;
            background-color: #0a192f;
        }
        #welcome-screen h1 {
            font-size: 1.8rem;
            margin-bottom: 20px;
            color: #64ffda;
        }
        .btn {
            background-color: #1d4ed8;
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
            background-color: #2563eb;
        }
        .question-box {
            display: none;
            background-color: #172a45;
            padding: 30px;
            border-radius: 10px;
            border: 1px solid #303c55;
            max-width: 400px;
            width: 100%;
        }
        .question-box h2 {
            font-size: 1.2rem;
            margin-bottom: 20px;
        }

        /* Dashboard-Layout */
        #dashboard {
            display: none;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
        }
        .dashboard-container {
            display: flex;
            width: 100%;
            height: 100%;
        }

        /* Linke Menüleiste */
        .sidebar {
            width: 240px;
            min-width: 240px;
            background-color: #172a45;
            height: 100%;
            border-right: 1px solid #303c55;
            transition: width 0.3s ease, min-width 0.3s ease, opacity 0.3s ease;
            overflow: hidden;
        }
        .sidebar.closed {
            width: 0;
            min-width: 0;
            opacity: 0;
            border-right: none;
        }
        .sidebar h2 {
            color: #64ffda;
            text-align: center;
            font-size: 1.1rem;
            margin-top: 20px;
            margin-bottom: 30px;
            white-space: nowrap;
        }
        .sidebar a {
            display: block;
            color: #cbd5e1;
            text-decoration: none;
            padding: 12px 20px;
            transition: background 0.2s, color 0.2s;
            white-space: nowrap;
            cursor: pointer;
        }
        .sidebar a:hover {
            background-color: #203a61;
            color: #ffffff;
        }

        /* Rechter Hauptbereich */
        .main-content {
            flex: 1;
            height: 100%;
            overflow-y: auto;
            overflow-x: hidden;
            padding: 20px;
            background-color: #0a192f;
        }
        .top-bar {
            display: flex;
            align-items: center;
            border-bottom: 1px solid #303c55;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
        .menu-toggle-btn {
            background-color: #1d4ed8;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 15px;
            font-size: 1rem;
        }
        .menu-toggle-btn:hover {
            background-color: #2563eb;
        }
        .top-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #f8fafc;
        }

        /* Sektionen im Dashboard */
        .content-section {
            display: none;
        }
        .content-section.active {
            display: block;
        }

        /* Admin Panel / Server-Verwaltung Styles */
        .server-card {
            background-color: #172a45;
            border: 1px solid #303c55;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .server-info h3 {
            margin: 0 0 5px 0;
            color: #64ffda;
            font-size: 1.1rem;
        }
        .server-info p {
            margin: 0;
            color: #94a3b8;
            font-size: 0.9rem;
        }
        .badge {
            background-color: #065f46;
            color: #34d399;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
        }
        .action-btn {
            background-color: #dc2626;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85rem;
        }
        .action-btn:hover {
            background-color: #b91c1c;
        }
    </style>
</head>
<body>

    <!-- Vorderseite / Startbildschirm mit Fragen -->
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

    <!-- Das eigentliche Dashboard -->
    <div id="dashboard">
        <div class="dashboard-container">
            <!-- Linke Menüleiste -->
            <div id="sidebar" class="sidebar">
                <h2>Phantom Menu</h2>
                <a onclick="switchTab('overview')">Übersicht</a>
                <a onclick="switchTab('settings')">Einstellungen</a>
                <a onclick="switchTab('stats')">Statistiken</a>
                <a onclick="switchTab('admin')" style="color: #64ffda; font-weight: bold;">🔒 Admin Panel (Owner)</a>
            </div>

            <!-- Rechter Hauptbereich -->
            <div id="main-content" class="main-content">
                <div class="top-bar">
                    <button class="menu-toggle-btn" onclick="toggleSidebar()">☰ Menü</button>
                    <div class="top-header" id="header-title">Übersicht</div>
                </div>

                <!-- Tab 1: Übersicht -->
                <div id="tab-overview" class="content-section active">
                    <p>Du hast alle Fragen beantwortet und bist erfolgreich auf dem Dashboard angekommen!</p>
                </div>

                <!-- Tab 2: Einstellungen -->
                <div id="tab-settings" class="content-section">
                    <p>Hier kannst du deine Dashboard-Einstellungen anpassen.</p>
                </div>

                <!-- Tab 3: Statistiken -->
                <div id="tab-stats" class="content-section">
                    <p>Hier siehst du allgemeine Statistiken des Systems.</p>
                </div>

                <!-- Tab 4: Admin Panel (Nur für den Owner - Bot Server Verwaltung) -->
                <div id="tab-admin" class="content-section">
                    <h2>Bot Server Verwaltung (Owner Panel)</h2>
                    <p style="color: #94a3b8; margin-bottom: 20px;">Übersicht aller Server, auf denen dein Bot aktiv ist:</p>
                    
                    <div class="server-card">
                        <div class="server-info">
                            <h3>Phantom Community Hub</h3>
                            <p>Mitglieder: 1,420 | Ping: 18ms</p>
                        </div>
                        <div>
                            <span class="badge">Online</span>
                            <button class="action-btn" onclick="alert('Bot von Server entfernt!')">Entfernen</button>
                        </div>
                    </div>

                    <div class="server-card">
                        <div class="server-info">
                            <h3>Gaming & Chill Lounge</h3>
                            <p>Mitglieder: 380 | Ping: 24ms</p>
                        </div>
                        <div>
                            <span class="badge">Online</span>
                            <button class="action-btn" onclick="alert('Bot von Server entfernt!')">Entfernen</button>
                        </div>
                    </div>

                    <div class="server-card">
                        <div class="server-info">
                            <h3>Phantom Test Server</h3>
                            <p>Mitglieder: 12 | Ping: 15ms</p>
                        </div>
                        <div>
                            <span class="badge">Online</span>
                            <button class="action-btn" onclick="alert('Bot von Server entfernt!')">Entfernen</button>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <script>
        function startQuiz() {
            document.getElementById('start-btn-container').style.display = 'none';
            document.getElementById('q1').style.display = 'block';
        }

        function nextQuestion(current, answer) {
            document.getElementById('q' + current).style.display = 'none';

            let next = current + 1;
            if (next <= 3) {
                document.getElementById('q' + next).style.display = 'block';
            } else {
                document.getElementById('welcome-screen').style.display = 'none';
                document.getElementById('dashboard').style.display = 'block';
            }
        }

        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('closed');
        }

        function switchTab(tabName) {
            // Alle Tabs verstecken
            document.querySelectorAll('.content-section').forEach(el => {
                el.classList.remove('active');
            });

            // Gewählten Tab anzeigen
            document.getElementById('tab-' + tabName).classList.add('active');

            // Header-Titel anpassen
            const titles = {
                'overview': 'Übersicht',
                'settings': 'Einstellungen',
                'stats': 'Statistiken',
                'admin': 'Admin Panel (Owner)'
            };
            document.getElementById('header-title').innerText = titles[tabName];
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
