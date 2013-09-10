from sassandsass.dbtools import *
from flask import g

class Editor:
    def __init__(self):
        self.script=()
        self.args={}
        self.COMMANDS = ('new', 'up', 'down', 'delete')
        self.CALLS = {
            'new' : 
                {'head' : ('INSERT INTO nav (head, rank, children) ' +
                    'VALUES (:head, :maxrank + 1, "");',),
                 'child' : ('UPDATE nav SET children = (children || ":id,") '+
                     'WHERE id = :parent')},
            'delete' :
                 {'head' : ('DELETE FROM nav WHERE id=:id',
                    'DELETE FROM nav WHERE id IN :children'),
                "child": ("DELETE FROM nav WHERE id=:id",
                    'UPDATE nav SET children = :children where id=:id')},
            'up': 
                {"head" : ("UPDATE nav SET rank = -1 where rank = :rank - 1",
                    'UPDATE nav SET rank = :rank - 1 WHERE rank = :rank',
                    'UPDATE nav SET rank = :rank WHERE rank = -1'),
                "child" : ('UPDATE nav SET children = :children '+
                    'WHERE id=:id',)},
            'down':
                {"head" : ("UPDATE nav SET rank = -1 where rank = :rank + 1",
                    'UPDATE nav SET rank = :rank + 1 WHERE rank = :rank',
                    'UPDATE nav SET rank = :rank WHERE rank = -1'),
                "child" : ('UPDATE nav SET children = :children '+
                    'WHERE id=:id',)}
                }
        self.max_rank=g.db.execute("SELECT max(rank) FROM nav").fetchone()

    def edit_nav(self, form):
        msg = self.process_form(form)
        if not self.script:
            return msg
        error = ""
        lines = []
        for line in self.script:
            lines.append(line)
            try:
                g.db.execute(line, self.args)
            except Exception as e:
                error = str(e)
                break
        if not error:
            g.db.commit()
        return "%s...%s" % (msg, "Success!" if not error else "\n"+error)

    def process_form(self, form):
        self.make_args(form)
        action = ""
        for key in form.keys():
            if key in self.COMMANDS:
                action = key
                break
        if action:
            msg = self.handle_action(action)
        else:
            msg="No Valid action in requesting form data."
        return msg

    def handle_action(self, action):
        actiontype = ("head" if self.args["head"] else "child")
        name = g.db.execute("SELECT title from pages where id = ?",
                            self.args["id"]).fetchall()
        if action == 'new':
            msg = "Attempting to add %s to navigation bar." % name
        elif action == 'up':
            if self.args["head"]:
                if self.args["rank"] == 1:
                    return "Item is already top rank."
            else:
                if self.args["id"]==self.siblings[0]:
                    return "Child is already top rank."
                i = self.siblings.index(self.args["id"])
                temp = self.siblings[i-1]
                self.siblings[i] = temp
                self.siblings[i-1] = self.args["id"]
                self.args["children"] = self.siblings.join(",")
            msg = "Attempting to move %s up one rank" % name 
        elif action == 'down':
            if self.args["head"]:
                if self.args["rank"] == self.max_rank:
                    return "Item is already lowest rank."
            else:
                if self.args["id"]==self.siblings[-1]:
                    return "Child is already lowest rank."
                i = self.siblings.index(self.args["id"])
                temp = self.siblings[i+1]
                self.siblings[i] = temp
                self.siblings[i+1] = self.args["id"]
                self.args["children"] = self.siblings.join(",")
            msg = "Attempting to move %s up one rank" % name
        elif action == 'delete':
            if not self.args["head"]:
                self.siblings.remove(self.args["id"])
                self.args["children"] = self.siblings.join(",")
            msg = "Attempting to delete %s from navigation bar." % name

        try:
            self.script = self.CALLS[action][actiontype]
        except KeyError:
            self.script = self.CALLS[action]
        return msg

                

    def make_args(self, form):
        for element in ["id","parent", "new"]:
            self.args[element] = (form[element] if element in form else "")
        self.args["head"] = (self.args["parent"] in ["", "-1"])
        if (self.args["parent"] not in [None, "-1"]):
            siblings = g.db.execute("SELECT children FROM nav WHERE id = ?",
                                        (self.args["parent"],)).fetchone()[0]
            self.siblings = siblings.split(',')[0:-1]
        elif self.args["id"]:
            rank = g.db.execute("SELECT rank FROM nav where id = ?",
                                    (self.args["id"],))
            self.args["rank"] = rank.fetchone()
            self.args["children"] = g.db.execute("SELECT children FROM nav "+
                                                "WHERE id = ?",
                                                 (self.args["id"],)).fetchone()
            if self.max_rank:
                self.args["maxrank"] = str(self.max_rank)
            else:
                self.args["maxrank"] = "0"
