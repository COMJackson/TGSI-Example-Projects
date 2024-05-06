from flask import Flask, render_template
from blog_data import BlogData

app = Flask(__name__)
blog_data = BlogData()

@app.route('/')
def get_home():
    blog_data.check_for_refresh()
    if not blog_data.ok:
        return render_template('error.html', error=blog_data.data)
    return render_template('index.html', data=blog_data.data)

@app.route('/about')
def get_about():
    return render_template('about.html', data=blog_data.data)

@app.route('/contact')
def get_contact():
    return render_template('contact.html', data=blog_data.data)

@app.route('/post/<int:p_id>')
def get_post(p_id):
    blog_data.check_for_refresh()
    if not blog_data.ok:
        return render_template('error.html', error=blog_data.data)
    sel_blog_data = None
    for data in blog_data.data:
        if data["id"] == p_id:
            sel_blog_data = data
    return render_template('post.html', post=sel_blog_data)

if __name__ == '__main__':
    app.run(debug=True)
