from flask import Flask,render_template,request,session,make_response
from src.models.user import User
from src.common.database import Database
from src.models.blog import  Blog
from src.models.post import  Post

app = Flask(__name__)  # __main__#
app.secret_key = "egze"


@app.route("/")
@app.route("/login")  # www.mysite.com/api/login
def login_template():
    return render_template("login.html")


@app.route("/register")  # www.mysite.com/api/register
def register_template():
    return render_template("register.html")


@app.route("/blogs/<string:user_id>")
@app.route("/blogs")
def user_blogs(user_id=None):
    print("geldim")
    if user_id is not None:
       user = User.get_by_id(user_id)
    else:
       user = User.get_by_email(session["email"])
    blogs = user.get_blog()
    return render_template("user_blogs.html",blogs= blogs,email= user.email)


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route("/auth/login", methods=["POST"])
def login_user():
    email = request.form["email"]
    password = request.form["password"]
    if User.login_valid(email, password):
       User.login(email)
    else:
       session["email"] = None

    return render_template("profile.html", email=session["email"])


@app.route("/auth/register",methods=["POST"])
def register_user():
   email = request.form["email"]
   password = request.form["password"]
   success = User.register(email, password)
   if(not success):
       session["email"] = None
   return render_template("profile.html", email=session["email"])



@app.route("/posts/<string:blog_id>")
def blog_post(blog_id):
    print("burfayimm")
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_post()
    return render_template("posts.html",posts = posts,blog_title = blog.title,blog_id = blog._id)


@app.route("/blogs/new",methods= ["POST","GET"])
def create_new_blog():
    if request.method == "GET" :
        return render_template("new_blog.html")
    else:
        title  = request.form["title"]
        description = request.form["description"]
        user = User.get_by_email(session["email"])
        new_blog = Blog(user.email,title,description,user.email)
        new_blog.save_to_mongo()
        #return make_response(user_blogs(user._id))
        return make_response(blog_post(new_blog._id))

@app.route("/posts/new/<string:blog_id>",methods= ["POST","GET"])
def create_new_post(blog_id):
    i=0
    print(i)
    if request.method == "GET" :
        print("Hellooooo")
        print(blog_id)
        return render_template("new_post.html",blog_id = blog_id)
    else :
        title  = request.form["title"]
        print(title)
        content = request.form["content"]
        print(content)
        user = User.get_by_email(session["email"])
        print(user.email)
        print(blog_id)
        new_post = Post(blog_id ,title,content,user.email)
        new_post.save_to_mongo()
        return make_response(blog_post(blog_id))


if __name__ == "__main__":
    app.run(port=30000)
