from flask import Flask, render_template, request, redirect, url_for
import subprocess
from datetime import datetime
import os
import sys

app = Flask(__name__)

def get_day_of_week(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%d')
    days = ['(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)']
    return days[date_object.weekday()]

def parse_txt():
    def convert_date_format(date_str):
        date_str = date_str.split('-')[1].strip()  # "- " 부분을 제거
        year = int(date_str.split('년')[0].strip())
        
        # "1(목)"과 같은 형식에서 숫자만 추출
        month_day = date_str.split('년')[1].split('/')
        month = int(month_day[0].strip())
        day = int(month_day[1].split('(')[0].strip())
        
        year += 2000  # "22년"을 "2022"로 변환
        return f"{year}-{month:02d}-{day:02d}"

    data = {}
    with open("./status.txt", "r", encoding = 'utf-8') as f:
        lines = f.readlines()

        timestamp = lines[0].strip().split(": ")[1]
        directory_path = lines[1].strip().split(": ")[1]

        data = {}
        category = None

        for line in lines:
            line = line.strip()

            if line.endswith('%)'):  # 카테고리를 확인하는 조건
                category = line.split('(')[0].strip()
                data[category] = []
            elif line.startswith('-'):
                date_str, value = line.split(':')
                date = convert_date_format(date_str)

                # Check for (labeled) and handle accordingly
                labeled = '(labeled)' in value
                if labeled:
                    value = value.replace('(labeled)', '').strip()
        
                if category:
                    data[category].append((date, int(value.strip()), labeled))
                else:
                    print("Error: No category detected")


    return timestamp, directory_path, data

timestamp, directory_path, data = parse_txt()
print("Timestamp:", timestamp)
print("Directory Path:", directory_path)
    
@app.route("/", methods=["GET", "POST"])
def index():
    selected_month = request.form.get('selected_month', default="all")

    timestamp, directory_path, data = parse_txt()

    if selected_month != "all":
        data = {
            key: [(date, value, labeled) for date, value, labeled in values if date.split('-')[1] == selected_month.zfill(2)]
            for key, values in data.items()
        }
    return render_template("index.html", timestamp=timestamp, directory_path=directory_path, data=data)

app.jinja_env.globals.update(get_day_of_week=get_day_of_week)

@app.route('/update', methods=['POST'])
def update():
    status_script_path = os.path.abspath("../status.py")
    print("Absolute path:", status_script_path)
    try:
        subprocess.run([sys.executable, status_script_path])
    except Exception as e:
        print(f"Error executing script: {e}")

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    
