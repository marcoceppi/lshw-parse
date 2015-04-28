#!/usr/bin/env python

class Dict(dict):
    def __getattr__(self, name):
        return self[name]


class Hardware(dict):
    def __init__(self, data, parent=None):
        self.__parse(data)

    def __parse(self, data, parent=None):
        name = self.__name(data, parent)
        for k, v in data.iteritems():
            if k in ('class', 'id'):
                continue
            if k == 'children':
                for child in v:
                    self.__parse(child, name)
            elif isinstance(v, dict):
                self.__parse(v, "%s.%s" % (name, k))
            else:
                self["%s.%s" % (name, k)] = v

    def __name(self, data, parent):
        """We don't get class or id before getting to children in __parse"""
        name = 'system'
        if 'class' not in data:
            return parent

        if data['class'] != name:
            name = data['id'].replace(':', '-')

        return "%s.%s" % (parent, name) if parent else name


class Package(Dict):
    @classmethod
    def parse(cls, pkg):
        if not 'name' in pkg:
            raise Exception('Invalid package data')

        return cls({'name': pkg.get('name'),
                    'version': pkg.get('version', None),
                    'description': pkg.get('desc', '')})


class Dpkg(Package):
    @classmethod
    def parse(cls, pkg):
        if not 'name' in pkg:
            raise Exception('Invalid package data')

        name = pkg['name']
        if ":%s" % pkg.get('arch') not in pkg['name']:
            name = "%s:%s" % (pkg.get('name'), pkg.get('arch'))

        return cls({'name': name,
                    'version': pkg.get('version'),
                    'description': pkg.get('desc', '')})


class Packages(dict):
    mapping = {'dpkg': Dpkg.parse}
    def __init__(self, data):
        if 'lshw' in data: del(data['lshw'])
        for k, v in data.iteritems():
            self[k] = [self.mapping.get(k, Package.parse)(p) for p in v]


class Profile(object):
    def __init__(self, profile):
        self.hardware = Hardware(profile['lshw'])
        self.packages = Packages(profile)

