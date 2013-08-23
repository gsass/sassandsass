from flask import Flask, render_template, url_for

app=Flask(__name__)

@app.route('/<name>')
def namedpage(name):
    return render_template('contentpage.html', name=name)

def create_resource_link(name, prefix="", **kwargs):
    #add a terminating slash if a prefix exists
    if prefix:
        prefix="%s/" % prefix
    link_attributes=['href', 'src']
    valid_link=False
    for attr in link_attributes:
        valid_link=valid_link or attr in kwargs
    if not valid_link:
        raise KeyError('A resource link requires a href or src attribute')
    attributes=['%s=\"%s\"' % (key, value) if key not in link_attributes 
                    else '%s=\"%s\"' % (key, url_for('static',  filename=''.join([prefix, value])) )
                    for key, value in kwargs]
    return "<%s %s />" % (name, ' '.join(attributes) )
    
if __name__ == '__main__':
    app.run(debug=True)
