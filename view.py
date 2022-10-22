from pprint import pprint
from flask import Flask, redirect, render_template

from forms.SearchForm import SearchForm
from api.searcher.search import Search_Long
from random import choice as ch
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    searcher = Search_Long()
    form = SearchForm()
    data = searcher.all("")
    theme_now = "glass"
    if form.validate_on_submit(): 
        return redirect(f"/search:{form.search.data}")
    return render_template(
         'search.html', form=form, links=data[0], img=data[1], wallpaper=ch(list(data[2].items())), theme_now=theme_now)

@app.route('/search:<string:title>', methods=['POST', 'GET'])
def search(title):
    searcher = Search_Long()
    form = SearchForm()
    data = searcher.all(title)
    theme_now = "glass"
    if form.validate_on_submit():
        return redirect(f"/search:{form.search.data}")
    return render_template(
        'search.html', form=form, links=data[0], img=data[1], wallpaper=ch(list(data[2].items())), theme_now=theme_now)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = "anime"
    app.run(host='127.0.0.1', debug=True)