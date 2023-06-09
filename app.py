from flask import Flask, request
import runpy
import requests
import time
import sys
import os
import subprocess
from os.path import exists
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route("/engine/execute", methods=['POST'])
def execute():
    result = {"status": False, "count": 0, "message": "", "err": ""}
    try:
        json = request.json
        file_name = "http://scheduler:3003/" + json["result"]["file_name"]
        # video_url = f"./videos/{file_name}"
        video_url = "./videos/" + file_name

        # file_exists = exists(video_url)
        is_file_exists = os.path.isfile(video_url)
        if (is_file_exists == True):
            # result["message"] = f"File {file_name} is already exists"
            result["message"] = "File" + file_name + " is already exists"

            return result
        # print(json['video_url'])

        # URL = "https://github.com/CN19-6310680233/cn332-arial-car-track/raw/main/video2.mp4"
        # ts = time.time()
        DownloadFile(json['video_url'], video_url)
        # --------
        # python detect.py --weights yolov7.pt --source "video2.mp4" --save-txt
        # --------
        # exec(open("script.py").read())
        # subprocess.call(shlex.split('./run-engine.sh'))
        # os.system(f"sh run-engine.sh {ts}.mp4")
        output_bytes = subprocess.check_output(
            [sys.executable, "./engine/cn332-arial-car-track/detect.py", "--weights", "yolov7.pt", "--source", video_url, "--save-txt"])
        output = output_bytes.decode('utf-8')
        res = output.split("[result]")
        # output = literal_eval(output_bytes.decode('utf-8'))
        print("OUTPUT -> ", output)
        # print(res)
        if (len(res) >= 2):
            # json_val = literal_eval(res[1])
            result["status"] = True
            # result["count"] = json_val["count"]
            result["count"] = res[1]
            result["message"] = "Execution successfully"
            # result = {
            #     "status": True,
            #     "count": res[-1]
            # }
            return result
        result["message"] = "Something went wrong with engine"
        return result
        # return {
        #     "status": False,
        #     "count": 0
        # }
    except Exception as e:
        print(e)
        print("<-- Exception -->")
        result["message"] = "Something went wrong, Unknown problem"
        result["err"] = e
        return result


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
