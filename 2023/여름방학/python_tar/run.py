## run.py (python3 run.py)
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import tarfile
import tempfile
import os.path
import io
import os

FLAG = "KEEPER{CVE_2007_4559_Is_a_S1mp1e_Vu1n_in_Python}"
COMPARE_STRING = "tar_tar_Tar_TAr_TaR_Tar"
TMP_FLAG_PATH = "/tmp/flag.txt"

app = Flask(__name__)
TEMP_DIR = tempfile.mkdtemp()

def check_tar(file_storage) -> bool:
    binary_data = file_storage.stream.read()
    binary_file = io.BytesIO(binary_data)

    try:
        with tarfile.open(fileobj=binary_file, mode="r") as tar:
            tar.extractall(TEMP_DIR)
        return True

    except:
        return False

def get_flag() -> str:
    try:
        with open(TMP_FLAG_PATH, "r") as f:
            data = f.read().strip()

            if data == COMPARE_STRING:
                return FLAG
            else:
                return ""

    except:
        return ""

@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files["file"]
    filename = secure_filename(f.filename)

    if os.path.exists(TMP_FLAG_PATH):
        os.remove(TMP_FLAG_PATH)

    if check_tar(f):
        f.save(os.path.join(TEMP_DIR, "output.tar"))
        msg = "파일이 저장되었습니다."
    else:
        msg = "파일 저장을 실패하였습니다."

    flag = get_flag()
    return render_template("index.html", msg = msg, flag = flag)

if __name__ == '__main__':
    app.run()
