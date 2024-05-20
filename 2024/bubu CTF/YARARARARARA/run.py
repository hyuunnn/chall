from flask import Flask, request
import yara
import string

app = Flask(__name__)
FLAG = string.punctuation * 10 + "BUBU{Yay3yaray3_whywhywhy!@!$%#}" + string.ascii_letters * 10

@app.route("/search/", methods=["POST"])
def search_post():
    rule = request.form.get("rule")
    if rule is None:
        return "No rule provided", 400

    rules = yara.compile(source=rule)
    matches = rules.match(data=FLAG)

    if matches:
        return f"Match {matches[0]}", 200
    else:
        return "No match", 200


@app.route("/search/", methods=["GET"])
def search_get():
    return """
    <form method="POST">
        <label for="rule">Enter your YARA rule:</label><br>
        <textarea name="rule" rows="20" cols="50"></textarea><br>
        <input type="submit" value="Submit">
    </form>
    """


@app.route("/")
def index():
    return 'Do you know Yara? <br> <a href="/search/">Search</a>'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
