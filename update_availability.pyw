from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Chromeオプションの設定
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 自動テストのメッセージを無効化
chrome_options.add_argument("--headless")  # ヘッドレスモード（UIなし）
chrome_options.add_argument("--disable-gpu")  # GPU無効化（ヘッドレスモードで推奨）
chrome_options.add_argument("--no-sandbox")  # サンドボックスを無効化（Linux環境で推奨）
chrome_options.add_argument("--disable-dev-shm-usage")  # メモリ不足回避のため

# chromedriverのサービス設定
service = Service()

# WebDriverの起動
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # マイページにアクセス
    print("マイページにアクセス中...")
    driver.get("https://daikonavi.com/mypage/")

    # ページの読み込み完了を確認
    WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    print("マイページの読み込み完了！")

    # ログインが必要な場合を想定
    if "ログイン" in driver.title:
        print("ログインページにリダイレクトされました。ログインを実行します。")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "id"))
        )
        username_field.send_keys("H3djXZSt")

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "pass"))
        )
        password_field.send_keys("P3caoCke")
        password_field.send_keys(Keys.RETURN)

        # ログイン後のページ読み込みを待機
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        print("ログイン成功！マイページに再度アクセスします。")
        driver.get("https://daikonavi.com/mypage/")
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # NEWS/空車更新ページに移動
    print("NEWS/空車更新リンクをクリック中...")
    news_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "NEWS/空車更新"))
    )
    news_link.click()

    WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    print("ニュースページに移動しました！")

    # 利用可能ボタンをクリック
    print("利用可能ボタンをクリック中...")
    activate_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "appealButton"))
    )
    driver.execute_script("arguments[0].click();", activate_button)
    print("利用可能ボタンがクリックされました！")

finally:
    # ブラウザを閉じる
    print("ブラウザを閉じます...")
    driver.quit()
