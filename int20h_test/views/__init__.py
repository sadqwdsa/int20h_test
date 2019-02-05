from int20h_test.views.home import HomeView


def setup(app):
    app.add_url_rule('/', view_func=HomeView.as_view('home'))
