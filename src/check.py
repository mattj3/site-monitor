import os
import json
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from notify import send_sms

load_dotenv()

RESULT_PATH = "results/past_results.json"
MAX_HOURS_OLD = 2

TARGET_URL = os.getenv("TARGET_URL")
SEARCH_TERM = os.getenv("SEARCH_TERM")
SEARCH_INPUT_SELECTOR = os.getenv("SEARCH_INPUT_SELECTOR")
RESULT_SELECTOR = os.getenv("RESULT_SELECTOR")

def load_previous():
    if not os.path.exists(RESULT_PATH):
        return None
    try:
        with open(RESULT_PATH, 'r') as f:
            data = json.load(f)
            age = (datetime.now(timezone.utc) - datetime.fromisoformat(data["timestamp"]).astimezone(timezone.utc))
            if age.total_seconds() / 3600 > MAX_HOURS_OLD:
                print(f"⚠️ Previous result is stale ({age.total_seconds() / 3600:.2f} hours old)")
            return data
    except Exception as e:
        print(f"❗ Could not read previous results: {e}")
        return None

def save_current(data):
    os.makedirs("results", exist_ok=True)
    with open(RESULT_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def run_check():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # uncomment if you want headless
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(TARGET_URL)
        
        time.sleep(1)

        try:
            result = driver.find_element(By.CLASS_NAME, RESULT_SELECTOR)
            result_text = result.text.strip()
            print(f"🔎 Found result with text: {result_text}")
        except Exception:
            print("🔎 No results found.")
            result_text = ""

        current_data = {"text": result_text, "timestamp": datetime.now().isoformat()}

        previous = load_previous()
        save_current(current_data)

        if previous and previous.get("text") != current_data["text"]:
            message = f"🔍 Result text changed:\nPrevious: {previous.get('text')}\nCurrent: {current_data['text']}\nSearch: {SEARCH_TERM}\nURL: {TARGET_URL}"
            send_sms(message)
        elif not previous:
            print("📥 First run or no previous data found.")
        else:
            print("✅ No change detected in result text.")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_check()
