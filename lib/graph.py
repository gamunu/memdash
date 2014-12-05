#!/usr/bin/env python3
'''Serve graphs'''

import cherrypy

class Graph(object):

    def __init__(self, db):
        self.database = db

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def hits(self, server):
        '''Returns hits graph data'''

        #get list of servers from sqlite database
        return self.database.get_hitsgraph(server)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def cmds(self, server):
        '''Returns cmds graph data'''

        return self.database.get_cmdgraph(server)
    
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def cacheditems(self, server):
        '''Returns cmds graph data'''

        return self.database.get_cacheditems(server)
    
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def memory(self, server):
        '''Returns cmds graph data'''

        return self.database.get_memory(server)