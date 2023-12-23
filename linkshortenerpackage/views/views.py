from flask import Flask, render_template, request, make_response, Blueprint, redirect
from database import test1, shorturl, get_long_website


views = Blueprint('views', __name__)


@views.route('/')
def homepage_route():
    return make_response(render_template('index.html', url=''))


@views.route('/submit-url/', methods=['POST'])
def submit_url_route():
    url = request.form['url_text']
    short_url = 'https://linkshortener-o50k.onrender.com/sl/'+shorturl(url)
    print(short_url)
    return make_response(render_template('index.html', url=short_url))


@views.route('/sl/<shorturl>')
def short_url_called(shorturl):
    url = get_long_website(shorturl)
    if url:
        return redirect(url)
    else:
        return render_template('error404.html')

