from flask import Flask, render_template, request, make_response, Blueprint, redirect
from ..database import url_shortener_collection, short_url, get_long_website
from dotenv import load_dotenv, dotenv_values
import validators

views = Blueprint(name='views', import_name=__name__)
load_dotenv()
env = dotenv_values()


@views.route('/', methods=['GET', 'POST'])
def homepage_route():
    url = ''
    if request.method == 'POST':
        url_txt = request.form['url_text']
        if validators.url(url_txt):
            url_prefix = env['SHORT_URL']
            url = url_prefix + short_url(url_txt)

    return make_response(render_template('index.html', url=url))


@views.route('/sl/<shorturl>')
def short_url_called(shorturl):
    url = get_long_website(shorturl)
    if url:
        return redirect(url)
    else:
        return render_template('error404.html')


@views.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html')


@views.errorhandler(500)
def internal_server_error(e):
    return render_template('error500.html')
