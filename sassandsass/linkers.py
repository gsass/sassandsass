from flask import url_for

def create_resource_link(name, prefix="", **kwargs):
    link_attributes = ['href', 'src']
    if not any([attr in kwargs for attr in link_attributes]):
        raise KeyError('A resource link requires a href or src attribute')
    attributes=['%s=\"%s\"' % (key, value) if key not in link_attributes 
                    else '%s=\"%s\"' % (key, url_for('static',  
                                        filename='/'.join([prefix, value])))
                    for key, value in kwargs.items()]
    if (name.lower() != "script"):
        return "<%s %s />" % (name, ' '.join(attributes) )
    else:
        return "<%s %s></%s>" % (name, ' '.join(attributes), name)
