#!/usr/bin/env python3
'''Serve graphs'''

import cherrypy
from model import graph

class Graph(object):
    
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def hits(self, server):
        '''Returns hits graph data'''

        # get list of servers from sqlite database
        return graph.Graph.get_hitsgraph(server)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def cmds(self, server):
        '''Returns cmds graph data'''

        return graph.Graph.get_cmdgraph(server)
    
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def cacheditems(self, server):
        '''Returns cmds graph data'''

        return graph.Graph.get_cacheditems(server)
    
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def memory(self, server):
        '''Returns cmds graph data'''

        return graph.Graph.get_memory(server)