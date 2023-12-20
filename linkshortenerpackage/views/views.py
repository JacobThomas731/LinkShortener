from flask import Flask, render_template, request, make_response, Blueprint

views = Blueprint('views', __name__)


@views.route('/')
def homepage_route():
    return make_response(render_template('index.html'))


@views.route('/submit-url/', methods=['POST'])
def submit_url_route():
    return make_response(render_template('<h1>Submit-url</h1>'))

# @views.route("/submiturl", methods=['POST'])
# def submit_url():
#     if request.method == 'POST':
#         url = request.form['url_text']
#         print(url + '123')
#     return make_response(render_template('index.html'))
