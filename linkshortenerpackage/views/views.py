from flask import Flask, render_template, request, make_response, Blueprint, redirect
from ..database import url_shortener_collection, short_url, get_long_website
from dotenv import load_dotenv, dotenv_values
import validators

views = Blueprint(name='views', import_name=__name__)
load_dotenv()
env = dotenv_values()


@views.route('/', methods=['GET', 'POST'])
def homepage_route():
    """
    This is the homepage route. This is also a redirect after the user presses the 'Generate' button
    :return: index html page. If user had pressed generate with a valid url, then the shortened url is also
    included in the index html page
    """
    url = ''
    if request.method == 'POST':
        url_txt = request.form['url_text']
        if validators.url(url_txt):
            url_prefix = env['SHORT_URL']
            url = url_prefix + short_url(url_txt) # short url generator called

    return make_response(render_template('index.html', url=url))


@views.route('/sl/<shorturl>')
def short_url_called(shorturl):
    """
    This function accepts the short url and redirects to the corresponding long url
    :param shorturl: the short url that is shared. Should include the prefix:
    https://linkshortener-o50k.onrender.com/sl/
    :return:redirects to long url or returns an error page
    """
    url = get_long_website(shorturl)
    if url:
        return redirect(url)
    else:
        return render_template('error404.html')


@views.errorhandler(404)
def page_not_found(e):
    """
    Error 404 when the required page is not found
    :param e: the exception
    :return: custom error404 html page
    """
    return render_template('error404.html')


@views.errorhandler(500)
def internal_server_error(e):
    """
    Error 500, generally when the server is down
    :param e: the exception
    :return: custom error500 html page
    """
    return render_template('error500.html')
