#!/usr/bin/env python


class Hardware(object):
    def __init__(self, data, parent=None):
        self.parent = parent or ""
        self.attr = {}
        self.children = None
        self.__parse(data)

    def __parse(self, data):
        for k, v in data.iteritems():
            if k == 'children':
                self.children = [Hardware(child, self.__name(data)) for child in v]
            else:
                self.attr[k] = v

    def __name(self, data=None):
        """We don't get class or id before getting to children in __parse"""
        if not data:
            data = self.attr
        name = 'system'
        if data['class'] != name:
            name = data['id'].replace(':', '-')

        return "%s.%s" % (self.parent, name) if self.parent else name

    def display(self):
        for k, v in self.attr.iteritems():
            if k in ('class', 'id'):
                continue
            if isinstance(v, dict):
                for kk, vv in v.iteritems():
                    # I know this is not very deep.
                    yield("%s.%s[%s]: %s" % (self.__name(), k, kk, vv))
            else:
                yield("%s.%s: %s" % (self.__name(), k, v))

        if self.children:
            for child in self.children:
                for c in child.display(): # This seems stupid.
                    yield c
