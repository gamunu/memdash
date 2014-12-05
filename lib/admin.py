#!/usr/bin/env python3
'''Admin interface functions'''

import cherrypy
from lib import html
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('views'))


class Admin(object):
    '''Admin interface functions'''

    def __init__(self, db):
        self.database = db

    @staticmethod
    @cherrypy.expose
    def index():
        '''Build the admin index page
        and return html
        @return: html string
        @rtype: str'''
        output_html = []

        index_html = env.get_template('admin.html')
        nav = html.Html.get_navigation('admin')
        return index_html.render({'title': "Admin", 'nav': nav})

    @cherrypy.expose
    def servers(self):
        '''Creates the table body rows
        and returns created html
        @return: html string
        @rtype: str'''
        output_html = []
        html_template = env.get_template('admin/table_row.html')
        for server in self.database.get_server_list():
            output_html.append(html_template.render({'server': server}))

        return ''.join(output_html)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def insert(self, name, port):
        '''Insert new server to database
        returns new inserted id
        @return: json object
        @rtype: str'''
        sid = 0
        if len(name) > 3 and port.isnumeric():
            sid = self.database.insert_server(name, port)
        return {'id':  sid}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def delete(self, sid):
        '''Delete a server from the database
        where sid equels to id
        @return: json object
        @rtype: str'''
        s_delete = False
        if sid.isnumeric() and int(sid) > 0:
            s_delete = self.database.delete_server(sid)
        return {'msg': s_delete}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update(self, name, port, sid):
        '''Update a server by setting new name and id
        where sid equels to id
        @return: json object
        @rtype: str'''
        s_update = False
        if sid.isnumeric() and int(sid) > 0:
            s_update = self.database.update_server(name, port, sid)

        return {'msg': s_update}
