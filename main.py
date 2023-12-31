from flask import Flask, render_template, request, send_from_directory
import requests
from smtplib import SMTP

def send_email(name, email, phone, message):
    my_email = "lewisjassy43@gmail.com"
    password = "lloiecglzazdbpgl"
    try:
        with SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            subject =  "Contact Form"
            body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
            connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=f"Subject:{subject}\n\n{body}")
    except Exception as e:
        print(f"Error sending email: {e}")


app = Flask(__name__)
response = requests.get(url="https://api.npoint.io/c790b4d5cab58020d391")
data = response.json()
posts = []

for post in data:
    post["image_url"] = f"./static/assets/img/cactus{post['id']}.avif"
    post_obj = (post["id"], post["title"], post["subtitle"], post["body"], post["image_url"])
    posts.append(post_obj)

@app.route("/")
def home():
    return render_template("index.html", all_posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        phone = data["phone"]
        email = data["email"]
        message = data["message"]
        send_email(name, email, phone, message)
        return render_template("contact.html", message="Successfully sent your message")
    return render_template("contact.html")

@app.route("/post/<int:post_id>")
def post(post_id):
    # Fetch the specific post based on post_id
    # You may want to modify this logic based on your data source
    selected_post = next((post for post in posts if post[0] == post_id), None)

    if selected_post:
        return render_template("post.html", post=selected_post, image=selected_post[4])
    else:
        # Handle case when the post with the given ID is not found
        return render_template("not_found.html")
    
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=False)
