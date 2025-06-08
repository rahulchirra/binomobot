import json
import os
import tkinter as tk
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from datetime import datetime
from random import randint
import requests
import matplotlib.pyplot as plt

# --- Telegram Config ---
TELEGRAM_TOKEN = "7446804468:AAH8LgjrU0JrmKrnWY8u5wjoUIFA16wJqXo"
TELEGRAM_CHAT_ID = "8127186541"
telegram_enabled = True

# --- Bot Logic ---
class BinomoBot:
    def __init__(self, email, password, comp_sets, update_ui):
        self.email = email
        self.password = password
        self.comp_sets = comp_sets
        self.current_set = 0
        self.compensation = comp_sets[self.current_set]
        self.driver = webdriver.Chrome(executable_path='./drivers/chromedriver')
        self.update_ui = update_ui
        self.running = True
        self.compen_index = 0
        self.wins = 0
        self.losses = 0
        self.initial_balance = 0
        self.balance_history = []

    def send_telegram(self, message):
        if telegram_enabled:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
                requests.post(url, data=data)
            except:
                pass

    def listen_telegram(self):
        offset = None
        while self.running:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
                if offset:
                    url += f"?offset={offset}"
                response = requests.get(url).json()
                for result in response.get("result", []):
                    offset = result["update_id"] + 1
                    text = result.get("message", {}).get("text", "")
                    if text == "/stop":
                        self.stop()
                        self.send_telegram("Bot stopped.")
                    elif text.startswith("/start"):
                        self.send_telegram("Bot already running.")
                sleep(5)
            except:
                pass

    def login(self):
        self.driver.get('https://id-binomo.com/auth')
        sleep(2)
        self.driver.find_element("xpath", '//*[@id="qa_auth_LoginEmailInput"]/vui-input/div[1]/div[2]/vui-input-text/input').send_keys(self.email)
        self.driver.find_element("xpath", '//*[@id="qa_auth_LoginPasswordInput"]/vui-input/div[1]/div[2]/vui-input-password/input').send_keys(self.password)
        self.driver.find_element("xpath", '//*[@id="qa_auth_LoginBtn"]/button').click()
        sleep(5)

    def checkbalance(self):
        try:
            balance = self.driver.find_element("xpath", '//*[@id="qa_trading_balance"]').text
            balance = balance.replace('Rp', '').replace('₮', '').replace(',', '').strip()[:-3]
            return int(balance)
        except:
            return 0

    def autoclick(self, compen):
        bid = self.driver.find_element("xpath", '//*[@id="amount-counter"]/div[1]/div[1]/vui-input-number/input')
        bid.send_keys(Keys.CONTROL, 'a')
        bid.send_keys(compen)
        sleep(2)

        if randint(0, 1) == 0:
            self.open_buy()
        else:
            self.open_sell()

    def open_buy(self):
        try:
            self.driver.find_element("xpath", '//*[@id="qa_trading_dealUpButton"]/button').click()
        except NoSuchElementException:
            self.driver.find_element("xpath", '//*[@id="analytics-demo"]/button').click()
            sleep(1)
            self.driver.find_element("xpath", '//*[@id="qa_trading_dealUpButton"]/button').click()

    def open_sell(self):
        try:
            self.driver.find_element("xpath", '//*[@id="qa_trading_dealDownButton"]/button').click()
        except NoSuchElementException:
            self.driver.find_element("xpath", '//*[@id="analytics-demo"]/button').click()
            sleep(1)
            self.driver.find_element("xpath", '//*[@id="qa_trading_dealDownButton"]/button').click()

    def run_bot(self):
        self.login()
        Thread(target=self.listen_telegram).start()
        sleep(10)
        self.initial_balance = self.checkbalance()
        previous_balance = self.initial_balance
        self.balance_history.append(self.initial_balance)
        self.autoclick(self.compensation[self.compen_index])

        while self.running:
            if datetime.now().second == 38:
                current_balance = self.checkbalance()
                profit = current_balance - self.initial_balance

                if current_balance > previous_balance:
                    self.compen_index = 0
                    self.wins += 1
                elif current_balance < previous_balance:
                    self.compen_index = min(self.compen_index + 1, len(self.compensation) - 1)
                    self.losses += 1

                previous_balance = current_balance
                self.balance_history.append(current_balance)
                self.update_ui(self.wins, self.losses, current_balance, profit)
                self.send_telegram(f"Balance: {current_balance} | Profit: {profit}")
                self.autoclick(self.compensation[self.compen_index])
            sleep(1)

    def stop(self):
        self.running = False
        self.plot_graph()
        self.driver.quit()

    def plot_graph(self):
        plt.plot(self.balance_history, marker='o')
        plt.title("Balance Over Time")
        plt.xlabel("Trades")
        plt.ylabel("Balance")
        plt.grid(True)
        plt.savefig("balance_graph.png")
        plt.close()

# --- GUI ---
class BotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Binomo Bot GUI")
        self.root.geometry("420x500")
        self.bot = None

        tk.Label(self.root, text="Email").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.pass_entry = tk.Entry(self.root, show="*")
        self.pass_entry.pack()

        tk.Label(self.root, text="Compensation Sets (e.g., 5,12|10,20)").pack()
        self.comp_entry = tk.Entry(self.root)
        self.comp_entry.insert(0, "5,12,32,78,195,488|10,20,40,80")
        self.comp_entry.pack()

        self.remember_var = tk.IntVar()
        tk.Checkbutton(self.root, text="Remember Me", variable=self.remember_var).pack()

        self.status = tk.Label(self.root, text="Wins: 0 | Losses: 0 | Balance: 0 | Profit: 0")
        self.status.pack(pady=10)

        tk.Button(self.root, text="Start Bot", command=self.start_bot).pack()
        tk.Button(self.root, text="Stop Bot", command=self.stop_bot).pack()

        self.load_credentials()
        self.root.mainloop()

    def load_credentials(self):
        if os.path.exists("credentials.json"):
            try:
                with open("credentials.json", "r") as f:
                    creds = json.load(f)
                    self.email_entry.insert(0, creds.get("email", ""))
                    self.pass_entry.insert(0, creds.get("password", ""))
            except:
                pass

    def save_credentials(self, email, password):
        with open("credentials.json", "w") as f:
            json.dump({"email": email, "password": password}, f)

    def update_ui(self, wins, losses, balance, profit):
        self.status.config(text=f"Wins: {wins} | Losses: {losses} | Balance: {balance} | Profit: {profit}")

    def start_bot(self):
        email = self.email_entry.get()
        pwd = self.pass_entry.get()
        raw_sets = self.comp_entry.get().split('|')
        comp_sets = [x.split(',') for x in raw_sets]

        if self.remember_var.get():
            self.save_credentials(email, pwd)

        self.bot = BinomoBot(email, pwd, comp_sets, self.update_ui)
        Thread(target=self.bot.run_bot).start()

    def stop_bot(self):
        if self.bot:
            self.bot.stop()

# --- Run GUI ---
if __name__ == "__main__":
    BotGUI()
