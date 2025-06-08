📌 BINOMO AUTO BOT GUIDE

🔧 REQUIREMENTS:
1. Python 3.x
2. Google Chrome or Brave browser (Version 137)
3. ChromeDriver (placed in /drivers folder)
4. Required Python libraries:
   - selenium
   - requests
   - matplotlib
   - playsound

Install libraries:
> pip install selenium requests matplotlib playsound

📁 PROJECT STRUCTURE:
├── main.py                # Main bot + GUI file
├── drivers/
│   └── chromedriver.exe   # Must match browser version
├── credentials.json       # Auto-created if "Remember Me" is checked
├── balance_graph.png      # Auto-generated graph after stop
└── README.txt             # You're reading it!

🚀 HOW TO RUN:
1. Open terminal in this folder.
2. Run:  python main.py
3. Enter your Binomo email, password.
4. Choose compensation sets (default ok: 5,12,32,78,195,488|10,20,40,80)
5. Check "Remember Me" (optional).
6. Click "Start Bot".

📲 TELEGRAM CONTROL:
- /stop  → Stop the bot
- /start → Check if bot is running

📈 AFTER TRADING:
- balance_graph.png file will show trade performance.

❗ IMPORTANT:
- Place correct chromedriver.exe inside /drivers
- Ensure browser version matches chromedriver version (v137)
