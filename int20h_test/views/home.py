from flask import render_template
from flask.views import View


class HomeView(View):

    def dispatch_request(self):
        return render_template('index.html')
