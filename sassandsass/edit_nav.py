from sassandsass.dbtools import *
from flask import g

class Editor:
    def __init__(self):
        self.script=()
        self.args={}
        self.CALLS = {
            'new' : 
                {'head' : ('INSERT INTO nav (id, head, rank, children) ' +
                    'VALUES (:id, :head, :maxrank + 1, "");',),
                    'child' : ('UPDATE nav SET children = :children '+
                     'WHERE id = :parent;',)},
            'delete' :
                 {'head' : ('DELETE FROM nav WHERE id=:id',
                    'DELETE FROM nav WHERE id IN (:children)',),
                "child": ("DELETE FROM nav WHERE id=:id",
                    'UPDATE nav SET children = :children where id=:parent',)},
            'up': 
                {"head" : ("UPDATE nav SET rank = -1 where rank = :rank - 1",
                    'UPDATE nav SET rank = :rank - 1 WHERE rank = :rank',
                    'UPDATE nav SET rank = :rank WHERE rank = -1',),
                "child" : ('UPDATE nav SET children = :children '+
                    'WHERE id=:parent',)},
            'down':
                {"head" : ("UPDATE nav SET rank = -1 where rank = :rank + 1",
                    'UPDATE nav SET rank = :rank + 1 WHERE rank = :rank',
                    'UPDATE nav SET rank = :rank WHERE rank = -1',),
                "child" : ("UPDATE nav SET children = :children "+
                    "WHERE id=:parent",)}
                }

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
        return "%s...%s" % (msg, "Success!" if not error 
                            else "; %s,Arguments passed were %s." 
                            % (error, self.args))

    def process_form(self, form):
        self.make_args(form)
        action = ""
        for key in form.keys():
            if key in self.CALLS:
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
            if self.args["head"]:
                msg = "Attempting to add %s to navigation bar." % name[0]
            else:
                msg = "Attempting to add %s as a child element." % name[0]
                self.siblings.append(self.args["id"])
                self.args["children"] = ",".join(self.siblings)
        elif action == 'up':
            if self.args["head"]:
                if self.args["rank"] == 1:
                    return "Item is already top rank."
            else:
                if self.siblings.index(self.args["id"]) == 0:
                    return "Child is already top rank."
                i = self.siblings.index(self.args["id"])
                temp = self.siblings[i-1]
                self.siblings[i] = temp
                self.siblings[i-1] = self.args["id"]
                self.args["children"] = ','.join(self.siblings)
            msg = "Attempting to move %s up one rank" % name[0] 
        elif action == 'down':
            if self.args["head"]:
                if self.args["rank"] == self.args["maxrank"]:
                    return "Item is already lowest rank."
            else:
                if self.siblings.index(self.args["id"]) == len(self.siblings)-1:
                    return "Child is already lowest rank."
                i = self.siblings.index(self.args["id"])
                temp = self.siblings[i+1]
                self.siblings[i] = temp
                self.siblings[i+1] = self.args["id"]
                self.args["children"] = ','.join(self.siblings)
            msg = "Attempting to move %s down one rank" % name[0]
        elif action == 'delete':
            if not self.args["head"]:
                self.siblings.remove(self.args["id"])
                self.args["children"] = ','.join(self.siblings)
            msg = "Attempting to delete %s from navigation bar." % name[0]
        #Assign the correct script to the script variable.
        try:
            self.script = self.CALLS[action][actiontype]
        except KeyError:
            self.script = self.CALLS[action]
        return msg

                

    def make_args(self, form):
        for element in ["id","parent", "new"]:
            self.args[element] = (form[element] if element in form else "")
        ishead = (self.args["parent"] in ["", "-1"])       
        self.args["head"] = ishead
        if not ishead:
            #If the element is a child, fetch parent element data.
            siblings = g.db.execute("SELECT children FROM nav WHERE id = ?",
                                        (self.args["parent"],)).fetchone()[0]
            if siblings:
                self.siblings = siblings.split(',')
            else:
                self.siblings = []
        else:
            #Try to operate on the element, or assign "" to the args.
            children = g.db.execute("SELECT children FROM nav "+
                                            "WHERE id = ?",
                                            (self.args["id"],)).fetchone()
            rank = g.db.execute("SELECT rank FROM nav "+
                                            "where id = ?",
                                            (self.args["id"],)).fetchone()
            for attr, request in (("children", children), ("rank", rank)):
                if request is not None:
                    self.args[attr] = request[0]
                else:
                    self.args[attr] = ""

        max_rank=g.db.execute("SELECT max(rank) FROM nav").fetchone()
        if max_rank:
            self.args["maxrank"] = str(max_rank[0])
        else:
            self.args["maxrank"] = "0"
