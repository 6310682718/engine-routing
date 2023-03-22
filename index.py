from flask import Flask, request
import wget
import runpy
import requests
import time
import sys
import os
import subprocess
from ast import literal_eval
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route("/engine/execute", methods=['POST'])
def execute():
    try:

        json = request.json
        # print(json['video_url'])
        # URL = "https://github.com/CN19-6310680233/cn332-arial-car-track/raw/main/video2.mp4"
        ts = time.time()
        # DownloadFile(json['video_url'], f"./videos/{ts}.mp4")
        # exec(open("script.py").read())
        # subprocess.call(shlex.split('./run-engine.sh'))
        # os.system(f"sh run-engine.sh {ts}.mp4")
        output_bytes = subprocess.check_output(
            [sys.executable, "script.py", "--weights", "yolov7.pt", "--source", "video2.mp"])
        output = literal_eval(output_bytes.decode('utf-8'))
        print("OUTPUT -> ", output['count'])
        return output
    except Exception as e:
        print(e)
        print("<-- Exception -->")
        return "Something went wrong !!"


def DownloadFile(url, filename=None):
    if filename is None:
        local_filename = url.split('/')[-1]
    else:
        local_filename = filename
    r = requests.get(url)
    f = open(local_filename, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            f.write(chunk)
    f.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
