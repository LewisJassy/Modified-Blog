from flask import Flask, render_template
import requests
app = Flask(__name__)
response = requests.get(url="https://api.npoint.io/c790b4d5cab58020d391")
data = response.json()
posts = []

for post in data:
    post["image_url"] = f"./static/assets/img/cactus{post['id']}.avif"
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

@app.route("/post/<int:post_id>")
def post(post_id):
    # Fetch the specific post based on post_id
    # You may want to modify this logic based on your data source
    selected_post = next((post for post in posts if post[0] == post_id), None)

    if selected_post:
        return render_template("post.html", post=selected_post)
    else:
        # Handle case when the post with the given ID is not found
        return render_template("not_found.html")

if __name__ == "__main__":
    app.run(debug=True)
