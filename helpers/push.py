
from datetime import datetime
from datetime import timedelta
import json
import os
import random

TOPIC_WORD_LIMIT = 300

tasks_file = 'files/in_progress.json'
backlog_file = 'files/backlog.json'

if not os.path.exists(tasks_file):
    if os.path.exists(backlog_file):
        tasks = json.load(open(backlog_file, "rt", encoding="UTF-8"))
        index_start = max(tasks, key=lambda task: task['index'])['index'] + 1
    else:
        tasks = []
        index_start = 1
    for root, dirs, files in os.walk('files/new'):
        for i, file in enumerate(files):
            input_file = f"{root}/{file}"
            data = json.load(open(input_file, "rt", encoding="UTF-8"))
            for item in data:
                task = { 
                    "index": i + index_start,
                    "domain": item['group'],
                    "name": item['problem'],
                    "description_prompt": f"Опиши проблему '{item['problem']}' из области '{item['group']}', не описывай решение, создай заголовок и выдели его одиночными обратными апострофами, сократи текст до тезизов 'Как было', 'Причины', 'Что сделано', 'Результат', используй не более {TOPIC_WORD_LIMIT} слов",
                    "description_image": f"Нарисуй рисунок, вдохновлённый проблемой '{item['problem']}' из области '{item['group']}'",
                    "solution_prompt": f"Опиши решение проблемы '{item['problem']}' с помощью техники '{item['technic']}' из области '{item['group']}', используй не более {TOPIC_WORD_LIMIT} слов",
                    "solution_image": f"Нарисуй рисунок, вдохновлённый темой '{item['technic']}' из области '{item['group']}'",
                    "group": f"{item['group']}/{item['technic']}",
                }
                tasks.append(task)
            processed_file = f"files/processed/{file}"
            os.rename(input_file, processed_file)

    year = datetime.today().year
    random.seed(year)
    random.shuffle(tasks)

    curr_date = datetime.today() + timedelta(days=1)
    for task in tasks:
        task["date"] = curr_date.strftime("%Y-%m-%d")
        curr_date += timedelta(days=3)

    json.dump(tasks, open(tasks_file, 'wt', encoding='UTF-8'), indent=4, ensure_ascii=False)
    if os.path.exists(backlog_file):
        os.remove(backlog_file)
    print(f"{len(tasks)} tasks created")
else: 
    print("Tasks already exists, revert before push")