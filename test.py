from flask import Flask, render_template
from flask_frozen import Freezer

app = Flask(__name__)
data = {
    'filename_one.html': 'value_one!',
    'filename_two.html': 'value_two!'
}

@app.route('/<path>/')
def dynamic_index(path):
    value = data[path]
    return render_template('./test_dynamic.html', value=value)

def generate_static_files(dynamic_paths):
    freezer = Freezer(app)
    app.config['FREEZER_RELATIVE_URLS'] = True
    app.config['FREEZER_DESTINATION'] = '../qiita/files'
    app.config['FREEZER_DESTINATION_IGNORE'] = [".git", ]

    @freezer.register_generator
    def product_url_generator():
        for path in dynamic_paths:
            yield "/" + path
    freezer.freeze()

if __name__ == "__main__":
    dynamic_paths = [
        'filename_one.html',
        'filename_two.html',
    ]
    generate_static_files(dynamic_paths)
