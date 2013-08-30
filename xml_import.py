from elementtree import ElementTree as et
from sys import stdin
import sqlite3


class XMLExtractor:
    def __init__(self):
        self.tree = None

    def load(self, eltree):
        self.tree = eltree

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

if __name__ == "__main__":
    fname = stdin.read().strip()
    xe = XMLExtractor()
    xe.load(et.parse(fname))
    print xe.extract("story")
