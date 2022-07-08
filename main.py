from flask import Flask, render_template

from parsers import print_djinni_data

app = Flask(__name__)


@app.route('/')
def home():
    return print_djinni_data()


if __name__ == '__main__':
    app.run()
