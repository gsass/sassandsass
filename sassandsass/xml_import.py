from elementtree import ElementTree as et
from sys import stdin
import sqlite3
from sassandsass import app
from flask import g


class XMLExtractor:
    '''A class to extract XML content from the old content.xml files used by the PHP site.'''
    def __init__(self):
        self.tree = None

    def load(self, eltree):
        self.tree = et.parse(eltree)

    def extract(self, chname):
        node = None
        for child in self.tree.getroot():
            print child.tag
            if child.tag == chname:
                node = child
                break
        if node:
            return self.get_text_content(node, chname)
        else:
            return ""

    def get_text_content(self, node, rootname):
        components = {}
        components["tag"] = node.tag
        components["tail"] = node.tail
        components["text"] = node.text
        components["attrib"] = ' '.join(
                                ['%s=%s' % (key, value)
                                    for key, value
                                    in node.attrib.items()])
        components["ctext"] = '\n'.join(
            [self.get_text_content(child, rootname)
                for child in node])

        for c in components:
            if components[c] is None:
                components[c] = ""
            else:
                components[c] = components[c].strip()

        if node.tag != rootname:
            return "<%(tag)s %(attrib)s>%(text)s%(ctext)s</%(tag)s>%(tail)s" \
                    % components
        else:
            return "%(text)s%(ctext)s%(tail)s" % components

    def import_page(self, page):
        self.load(page)
        fields = {}
        for field in ['title', 'blurb', 'imagename', 'content']:
            fields[field] = self.extract(field)
        g.db.execute('INSERT INTO pages (?) VALUES ?', ",".join(fields.keys()), ",".join(fields.values))
        g.db.commit()

if __name__ == "__main__":
    '''reads one or more filenames writted to stdio, and imports them into the app db.
    
    Recommended use: ls [your content folder] | python xml_import.py'''
    fnames = stdin.readlines()
    xe = XMLExtractor()
    for line in fnames:
        line=line.strip()
        xe.import_page(line)
