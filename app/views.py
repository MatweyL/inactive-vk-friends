from flask import Flask, render_template, request
from analize.analize_profile import ProfileAnalizer

from dotenv_utils import get_host, get_port

app = Flask(__name__)
page_analizer = ProfileAnalizer()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        result = None
        if request.form.get("profile_link"):
            link = request.form.get("profile_link")
            result = page_analizer.analize_by_photos(link[link.rfind("/") + 1:])
            # print(result)
        return render_template("index.html", result=result)
    else:
        return render_template("index.html")


def run_flask():
    app.run(host=get_host(), port=get_port(), debug=True)
