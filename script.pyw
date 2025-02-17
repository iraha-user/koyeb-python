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

# WebDriverの起動
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # ニュースページにアクセス
    print("ニュースページにアクセス中...")
    driver.get("https://daikonavi.com/mypage/news.php")

    # ログインページの場合、ログインを実行
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
        password_field.send_keys(Keys.RETURN)
        print("ログイン成功！ニュースページに再度アクセスします。")
        driver.get("https://daikonavi.com/mypage/news.php")
    
    print("ニュースページの読み込み完了！")

    # タイトルフィールドに入力
    print("NEWSタイトルを入力中...")
    title_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    )
    title_field.clear()
    title_field.send_keys("〇年中無休で営業中〇")

    # NEWS内容フィールドに入力
    print("NEWS内容を入力中...")
    content_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "body"))
    )
    content_field.clear()
    content_field.send_keys("〇本日も元気に営業中(^^♪")

    # 更新ボタンをクリック
    print("NEWS更新ボタンをクリック中...")
    update_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='NEWS更新ボタン >']"))
    )
    update_button.click()
    print("更新ボタンをクリックしました！")

    # ポップアップの処理
    print("ポップアップを処理中...")
    WebDriverWait(driver, 10).until(EC.alert_is_present())  # ポップアップの表示待機
    alert = driver.switch_to.alert  # JavaScriptアラートを切り替え
    print(f"ポップアップメッセージ: {alert.text}")  # ポップアップのメッセージを表示

    # OKボタンをクリック
    alert.accept()
    print("OKボタンをクリックしました！")

    # 必要に応じてポップアップが閉じるのを待機
    WebDriverWait(driver, 10).until(EC.staleness_of(driver.find_element(By.TAG_NAME, "body")))
    print("ポップアップが閉じました。")

    print("NEWSの更新が完了しました！")

except Exception as e:
    print("エラーが発生しました:", e)

finally:
    # ブラウザを閉じる
    print("ブラウザを閉じます...")
    driver.quit()
