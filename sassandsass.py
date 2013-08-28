from flask import Flask, render_template, url_for
from linkers import create_resource_link

app=Flask(__name__)
app.jinja_env.globals.update(create_resource_link=create_resource_link)

@app.route('/<name>')
def namedpage(name):
    return render_template('content.html', name=name)
 
if __name__ == '__main__':
    app.run(debug=True)
