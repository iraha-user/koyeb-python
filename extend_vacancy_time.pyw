from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Chromeオプションの設定（UIなし）
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # UIなしで実行
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920x1080")  # 画面サイズを指定

# WebDriverの起動
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # ログインページにアクセス
    print("ページにアクセス中...")
    driver.get("https://daikonavi.com/mypage/news.php")

    # ページの読み込み完了を待機
    WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")

    # ログイン処理
    if "業者ログイン" in driver.title:
        print("ログインページにリダイレクトされました。ログインを実行します。")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "id"))
        )
        username_field.send_keys("H3djXZSt")

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "pass"))
        )
        password_field.send_keys("P3caoCke")
        password_field.send_keys(Keys.RETURN)  # Enterキーでログイン
        print("ログイン成功！ページに再アクセスします。")
        driver.get("https://daikonavi.com/mypage/news.php")
        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")

    # 「時間延長」ボタンを探してクリック
    print("時間延長ボタンを探しています...")
    extend_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '時間延長')]"))
    )
    driver.execute_script("arguments[0].click();", extend_button)
    print("時間延長ボタンをクリックしました！")

except Exception as e:
    print(f"エラーが発生しました: {e}")

finally:
    # ブラウザを閉じる
    print("ブラウザを閉じます...")
    driver.quit()
