import time
import subprocess
from datetime import datetime, timedelta
import os

def update_start_time():
    """ 毎日 19:00 に start_time を更新 """
    now = datetime.now()
    return now.replace(hour=19, minute=0, second=0, microsecond=0)

def calculate_next_run(current_time, interval_seconds):
    """ 次回の実行時間を正しく計算（24時間対応） """
    return current_time + timedelta(seconds=interval_seconds)

# start_time を毎日更新
start_time = update_start_time()

# script.pyw の実行
def run_script():
    print(f"現在時刻: {datetime.now()} - script.pyw を実行します。")
    try:
        subprocess.run(["pythonw", "C:/Users/iraha/Desktop/script.pyw"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"script.pyw 実行中にエラーが発生しました: {e}")

def run_update_availability():
    try:
        subprocess.run(["pythonw", "C:/Users/iraha/Desktop/update_availability.pyw"], check=True)
    except subprocess.CalledProcessError:
        pass

def run_extend_vacancy_time():
    try:
        subprocess.run(["pythonw", "C:/Users/iraha/Desktop/extend_vacancy_time.pyw"], check=True)
    except subprocess.CalledProcessError:
        pass

# スケジュールの監視
def monitor_schedule():
    print("スケジュール管理を開始します。")

    next_script_run = calculate_next_run(datetime.now(), 31 * 60)
    next_availability_run = calculate_next_run(datetime.now(), 15 * 60 + 20)
    next_extend_run = calculate_next_run(datetime.now(), 4 * 60)

    while True:
        current_time = datetime.now()

        # 毎日 19:00 に start_time を更新
        if current_time.hour == 19 and current_time.minute == 0:
            global start_time
            start_time = update_start_time()
            print("🔄 start_time を更新しました。")

        # script.pyw の実行
        if current_time >= next_script_run:
            run_script()
            next_script_run = calculate_next_run(current_time, 31 * 60)

        # update_availability.pyw の実行（ログなし）
        if current_time >= next_availability_run:
            run_update_availability()
            next_availability_run = calculate_next_run(current_time, 15 * 60 + 20)

        # extend_vacancy_time.pyw の実行（ログなし）
        if current_time >= next_extend_run:
            run_extend_vacancy_time()
            next_extend_run = calculate_next_run(current_time, 4 * 60)

        # スリープして次の確認を待つ
        time.sleep(1)

# スケジュールの監視を開始
if __name__ == "__main__":
    try:
        monitor_schedule()
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        print("タスクスケジューラーのタスクを終了します...")
        os.system('schtasks /end /tn "Pythonスケジュール実行"')
