from flask import Flask, render_template
import requests
app = Flask(__name__)
response = requests.get(url="https://api.npoint.io/c790b4d5cab58020d391")
data = response.json()
posts = []

for post in data:
    post_obj = (post["id"], post["title"], post["subtitle"], post["body"])
    posts.append(post_obj)

@app.route("/")
def home():
    return render_template("index.html", all_posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)