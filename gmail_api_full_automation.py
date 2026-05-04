from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random
import string
import json
import os
from pathlib import Path
import requests

class GmailAPIFullAutomator:
    def __init__(self, gmail_email, gmail_password):
        self.email = gmail_email
        self.password = gmail_password
        self.random_app_name = self.generate_random_name()
        self.setup_driver()
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_random_name(self):
        """Random app name generate"""
        adjectives = ['QuickMail', 'FastAPI', 'SmartGmail', 'ProMail', 'EasyAPI', 'CloudBot']
        numbers = random.randint(1000, 9999)
        return f"{random.choice(adjectives)}{numbers}"
    
    def setup_driver(self):
        """Chrome driver with stealth mode"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)
        
    def login_gmail(self):
        """Step 1: Gmail login"""
        print("🔐 [1/15] Gmail login করছে...")
        self.driver.get("https://accounts.google.com/signin")
        time.sleep(3)
        
        # Email
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
        email_input.send_keys(self.email)
        self.driver.find_element(By.ID, "identifierNext").click()
        time.sleep(4)
        
        # Password  
        password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
        password_input.send_keys(self.password)
        self.driver.find_element(By.ID, "passwordNext").click()
        time.sleep(6)
        print("✅ Login successful!")
    
    def go_cloud_console(self):
        """Step 2: Cloud Console"""
        print("☁️ [2/15] Google Cloud Console...")
        self.driver.get("https://console.cloud.google.com/")
        time.sleep(5)
    
    def select_country_us(self):
        """Step 3: Country US + I Agree"""
        print("🌎 [3/15] Country United States select...")
        try:
            country_select = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "select[aria-label*='Country']"))
            )
            country_select.click()
            time.sleep(1)
            us_option = self.driver.find_element(By.XPATH, "//option[contains(text(),'United States')]")
            us_option.click()
            time.sleep(1)
            
            agree_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'I agree')] | //button[contains(text(),'Agree')]")
            self.driver.execute_script("arguments[0].click();", agree_btn)
            time.sleep(3)
            print("✅ Country selected!")
        except:
            print("⚠️ Country already set")
    
    def enable_gmail_api(self):
        """Step 4: Gmail API enable"""
        print("📧 [4/15] Gmail API enable করছে...")
        search_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Search'], input[placeholder*='Search']")))
        search_box.clear()
        search_box.send_keys("Gmail API")
        time.sleep(2)
        
        gmail_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Gmail API') or contains(text(),'gmail')]")))
        gmail_link.click()
        time.sleep(4)
        
        enable_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Enable') or contains(text(),'ENABLE')]")))
        self.driver.execute_script("arguments[0].click();", enable_btn)
        time.sleep(6)
        print("✅ Gmail API enabled!")
    
    def go_api_service_details(self):
        """Step 5: API & Services → OAuth Consent Screen"""
        print("⚙️ [5/15] API & Services → OAuth...")
        try:
            # APIs & Services menu
            apis_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'APIs & Services')]")))
            self.driver.execute_script("arguments[0].click();", apis_menu)
            time.sleep(2)
            
            oauth_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'OAuth consent screen')]")))
            oauth_link.click()
            time.sleep(4)
        except:
            self.driver.get("https://console.cloud.google.com/apis/credentials/consent")
            time.sleep(4)
        print("✅ OAuth Consent Screen page!")
    
    def oauth_consent_setup(self):
        """Step 6-10: OAuth Consent Screen full setup"""
        print("🔐 [6-10/15] OAuth Consent Screen setup...")
        
        # Get Started
        try:
            get_started = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Get started')]")))
            get_started.click()
            time.sleep(3)
        except:
            pass
        
        # App Name + Support Email
        app_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label*='App name'], input[aria-label*='name']")))
        app_name.clear()
        app_name.send_keys(self.random_app_name)
        print(f"📝 App Name: {self.random_app_name}")
        
        support_email = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label*='support'], input[aria-label*='Support']")
        support_email.clear()
        support_email.send_keys(self.email)
        
        next_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'Next')]")
        next_btn.click()
        time.sleep(3)
        
        # Audience → External
        external_radio = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//md-radio-button[contains(@aria-label,'External')] | //label[contains(text(),'External')]")))
        self.driver.execute_script("arguments[0].click();", external_radio)
        time.sleep(2)
        next_btn.click()
        time.sleep(3)
        
        # Contact Information
        contact_email = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label*='Email'], input[aria-label*='email']")))
        contact_email.clear()
        contact_email.send_keys(self.email)
        next_btn.click()
        time.sleep(3)
        
        # I Agree + Finish
        agree_cb = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//md-checkbox[contains(@aria-label,'I agree')]")))
        self.driver.execute_script("arguments[0].click();", agree_cb)
        time.sleep(1)
        
        finish_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'Finish')]")
        finish_btn.click()
        time.sleep(4)
        
        continue_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue') or contains(text(),'CONFIRM')]")))
        continue_btn.click()
        time.sleep(4)
        print("✅ OAuth setup complete!")
    
    def add_test_user(self):
        """Step 11: Test Users add"""
        print("👥 [11/15] Test user add করছে...")
        test_users_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Test users')] | //span[contains(text(),'Test users')]")))
        test_users_tab.click()
        time.sleep(3)
        
        add_users_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add users')]")))
        add_users_btn.click()
        time.sleep(2)
        
        email_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='email'], input[aria-label*='email']")))
        email_input.send_keys(self.email)
        time.sleep(1)
        
        save_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'Save')]")
        save_btn.click()
        time.sleep(3)
        print("✅ Test user added!")
    
    def publish_app(self):
        """Step 12: Publish App"""
        print("📤 [12/15] App publish...")
        publish_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Publish App')] | //span[contains(text(),'Publish')]")))
        self.driver.execute_script("arguments[0].click();", publish_btn)
        time.sleep(3)
        
        confirm_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Confirm') or contains(text(),'Publish')]")))
        confirm_btn.click()
        time.sleep(5)
        print("✅ App published!")
    
    def create_oauth_client(self):
        """Step 13-15: Create Client → Desktop → Download JSON"""
        print("🔑 [13-15/15] OAuth Client + JSON download...")
        
        # Go to Credentials
        credentials_tab = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Credentials')]")))
        credentials_tab.click()
        time.sleep(4)
        
        # Create Credentials → OAuth Client
        create_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Create Credentials')]")))
        self.driver.execute_script("arguments[0].click();", create_btn)
        time.sleep(2)
        
        oauth_client = self.driver.find_element(By.XPATH, "//md-option[contains(text(),'OAuth client ID')]")
        oauth_client.click()
        time.sleep(3)
        
        # Desktop app
        app_type_select = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "md-select[aria-label*='Application type']")))
        app_type_select.click()
        time.sleep(1)
        
        desktop_option = self.driver.find_element(By.XPATH, "//md-option[contains(text(),'Desktop application')]")
        desktop_option.click()
        time.sleep(2)
        
        # Create
        create_final = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Create')]")))
        create_final.click()
        time.sleep(5)
        
        # Download JSON (popup থেকে)
        download_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'.json') or contains(text(),'Download JSON')]")))
        json_url = download_link.get_attribute("href")
        
        # JSON download & save
        response = requests.get(json_url)
        json_path = self.output_dir / "gmail_api_credentials.json"
        with open(json_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ [COMPLETE!] JSON saved: {json_path}")
        print(f"📋 App Name: {self.random_app_name}")
        print("🎉 Full automation successful!")
    
    def run_complete_flow(self):
        """Full 15 steps automation"""
        steps = [
            self.login_gmail,
            self.go_cloud_console,
            self.select_country_us,
            self.enable_gmail_api,
            self.go_api_service_details,
            self.oauth_consent_setup,
            self.add_test_user,
            self.publish_app,
            self.create_oauth_client
        ]
        
        for i, step in enumerate(steps, 1):
            try:
                step()
                print(f"⏳ Waiting 2s...")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Step {i} failed: {str(e)}")
                print("🔄 Retrying in 5s...")
                time.sleep(5)
                continue
        
        print("\n🎊 ALL STEPS COMPLETE!")
        print(f"📁 Output folder: {self.output_dir}")
        input("\nEnter চেপে browser বন্ধ করুন...")

# 🚀 RUN
if __name__ == "__main__":
    # আপনার credentials এখানে দিন
    EMAIL = input("📧 Gmail: ") or "your_email@gmail.com"
    PASSWORD = input("🔑 App Password: ") or "your_app_password"
    
    print("🚀 Gmail API Full Automation Starting...")
    print("⚠️  CAPTCHA manually solve করতে হবে!")
    
    automator = GmailAPIFullAutomator(EMAIL, PASSWORD)
    automator.run_complete_flow()
