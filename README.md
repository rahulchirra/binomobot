# 📌 BINOMO AUTO BOT GUIDE

---

## 🔧 REQUIREMENTS:

1. **Python 3.x**
2. **Google Chrome or Brave browser** (Version 137)
3. **ChromeDriver** (placed in `/drivers` folder)
4. Required Python libraries:
   - `selenium`
   - `requests`
   - `matplotlib`
   - `playsound`

📦 Install all libraries using:
```bash
pip install selenium requests matplotlib playsound
```

---

## 📁 PROJECT STRUCTURE:

```
BinomoBot/
├── main.py                # Main bot + GUI file
├── drivers/
│   └── chromedriver.exe   # Must match browser version
├── credentials.json       # Auto-created if "Remember Me" is checked
├── balance_graph.png      # Auto-generated graph after stop
└── README.md              # You're reading it!
```

---

## 🚀 HOW TO RUN:

1. Open **terminal** in this folder.
2. Run the bot:
   ```bash
   python main.py
   ```
3. Enter your **Binomo email** and **password** in the GUI.
4. Compensation sets (default is good):  
   `5,12,32,78,195,488|10,20,40,80`
5. Check ✅ **"Remember Me"** (optional).
6. Click **"Start Bot"**.

---

## 📲 TELEGRAM CONTROL:

| Command | Action            |
|---------|-------------------|
| `/start` | Check if bot is running |
| `/stop`  | Stop the bot           |

> Make sure to enter your Telegram `token` and `chat_id` in the code.

---

## 📈 AFTER TRADING:

- `balance_graph.png` will be saved showing your **performance graph**.

---

## ❗ IMPORTANT NOTES:

- Make sure the **chromedriver.exe** is placed inside `drivers/`.
- It **must match** the browser version (**v137** for Brave/Chrome).
- `credentials.json` is **auto-generated** when "Remember Me" is selected.

---

✅ You're now ready to auto-trade on Binomo with full GUI, alerts, Telegram, and graphs!