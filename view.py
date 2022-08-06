import pprint
from flask import Flask, redirect, render_template

from forms.SearchForm import SearchForm
from api.searcher.search import Search_Long
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f"/search:{form.search.data}")
    return render_template(
        'layout.html', form=form)

@app.route('/search:<string:title>', methods=['POST', 'GET'])
def search(title):
    searcher = Search_Long()
    form = SearchForm()
    data = searcher.anime_go_and_zoro_to(title)
    if form.validate_on_submit():
        return redirect(f"/search:{form.search.data}")
    return render_template(
        'search.html', form=form, links=data[0], img=data[1])


if __name__ == '__main__':
    app.config['SECRET_KEY'] = "anime"
    app.run(port=8080, host='127.0.0.1', debug=True)