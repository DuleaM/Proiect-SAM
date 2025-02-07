from flask import Flask
import requests
import schedule
import time
import threading

app = Flask(__name__)

def send_post_request():
    url = 'http://127.0.0.1:8000/playstore/api/update-top-apps/'
    response = requests.post(url)
    print(f'Response from Django: {response.text}')

schedule.every(1).minutes.do(send_post_request)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/')
def home():
    return "Flask app is running!"

if __name__ == '__main__':
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()
    app.run(host='0.0.0.0', port=5001)