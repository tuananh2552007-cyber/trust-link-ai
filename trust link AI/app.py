from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    

    results = []

    if request.method == "POST":

        urls = []

        text_input = request.form.get("urls")

        if text_input:
            urls.extend(text_input.splitlines())

        file = request.files.get("file")

        if file and file.filename.endswith(".txt"):

            content = file.read().decode("utf-8")

            urls.extend(content.splitlines())

        for url in urls:

            url = url.strip()

            if url:

                try:

                    response = requests.get(url, timeout=5)

                    if response.status_code == 200:
                        status = "Hoạt động"

                    elif response.status_code in [301, 302]:
                        status = "Chuyển hướng"

                    else:
                        status = "Lỗi"

                    results.append({
                        "url": url,
                        "status": status,
                        "code": response.status_code
                    })

                except:

                    results.append({
                        "url": url,
                        "status": "Không hoạt động",
                        "code": "Error"
                    })

    return render_template("index.html", results=results)
from flask import jsonify

@app.route("/ai-check", methods=["POST"])
def ai_check():
    data = request.get_json()
    urls_text = data.get("urls", "")

    urls = urls_text.splitlines()

    results = []

    for url in urls:
        url = url.strip()
        if not url:
            continue

        try:
            response = requests.get(url, timeout=5)

            # 🤖 AI logic đơn giản
            if "login" in url or "bank" in url:
                status = "⚠️ Nghi ngờ (AI cảnh báo)"
            elif response.status_code == 200:
                status = "Hoạt động"
            elif response.status_code in [301, 302]:
                status = "Chuyển hướng"
            else:
                status = "Lỗi"

            results.append({
                "url": url,
                "status": status,
                "code": response.status_code
            })

        except:
            results.append({
                "url": url,
                "status": "Không hoạt động",
                "code": "Error"
            })

    return jsonify(results)
if __name__ == "__main__":
    app.run(debug=True)