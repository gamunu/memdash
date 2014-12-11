#!/usr/bin/env python3
'''Serve graphs'''

import cherrypy
from model import graph
import datetime
from cherrypy import log

class Graph(object):
    
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def hits(self, server, startdate = None, enddate = None):
        '''Returns hits graph data'''
        
        if not (startdate and enddate):
            startdate = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            startdate = datetime.datetime.fromtimestamp(int(startdate)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.fromtimestamp(int(enddate)).strftime('%Y-%m-%d %H:%M:%S')

        # get list of servers from sqlite database
        return graph.Graph.get_hitsgraph(server, startdate, enddate)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def cmds(self, server, startdate = None, enddate = None):
        '''Returns cmds graph data'''
        if not (startdate and enddate):
            startdate = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            startdate = datetime.datetime.fromtimestamp(int(startdate)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.fromtimestamp(int(enddate)).strftime('%Y-%m-%d %H:%M:%S')

        return graph.Graph.get_cmdgraph(server, startdate, enddate)
    
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def cacheditems(self, server, startdate = None, enddate = None):
        '''Returns cmds graph data'''

        if not (startdate and enddate):
            startdate = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            startdate = datetime.datetime.fromtimestamp(int(startdate)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.fromtimestamp(int(enddate)).strftime('%Y-%m-%d %H:%M:%S')

        return graph.Graph.get_cacheditems(server, startdate, enddate)
    
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def memory(self, server, startdate = None, enddate = None):
        '''Returns cmds graph data'''

        if not (startdate and enddate):
            startdate = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            startdate = datetime.datetime.fromtimestamp(int(startdate)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.fromtimestamp(int(enddate)).strftime('%Y-%m-%d %H:%M:%S')

        return graph.Graph.get_memory(server, startdate, enddate)
    
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def responsetime(self, server, startdate = None, enddate = None):
        '''Returns cmds graph data'''

        if not (startdate and enddate):
            startdate = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            startdate = datetime.datetime.fromtimestamp(int(startdate)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.fromtimestamp(int(enddate)).strftime('%Y-%m-%d %H:%M:%S')

        return graph.Graph.get_responsetime(server, startdate, enddate)
    
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def ovhits(self, startdate = None, enddate = None):
        '''Returns hits graph data'''

        if not (startdate and enddate):
            startdate = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            startdate = datetime.datetime.fromtimestamp(int(startdate)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.fromtimestamp(int(enddate)).strftime('%Y-%m-%d %H:%M:%S')

        # get list of servers from sqlite database
        return graph.Graph.overall_hitsgraph(startdate, enddate)

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def ovcmds(self, startdate = None, enddate = None):
        '''Returns cmds graph data'''

        if not (startdate and enddate):
            startdate = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            startdate = datetime.datetime.fromtimestamp(int(startdate)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.fromtimestamp(int(enddate)).strftime('%Y-%m-%d %H:%M:%S')

        return graph.Graph.overall_cmdgraph(startdate, enddate)
    
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def ovcacheditems(self, startdate = None, enddate = None):
        '''Returns cmds graph data'''

        if not (startdate and enddate):
            startdate = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            startdate = datetime.datetime.fromtimestamp(int(startdate)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.fromtimestamp(int(enddate)).strftime('%Y-%m-%d %H:%M:%S')

        return graph.Graph.overall_cacheditems(startdate, enddate)
    
    @cherrypy.tools.json_out()
    @cherrypy.expose
    def ovmemory(self, startdate = None, enddate = None):
        '''Returns cmds graph data'''

        if not (startdate and enddate):
            startdate = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            startdate = datetime.datetime.fromtimestamp(int(startdate)).strftime('%Y-%m-%d %H:%M:%S')
            enddate =  datetime.datetime.fromtimestamp(int(enddate)).strftime('%Y-%m-%d %H:%M:%S')

        return graph.Graph.overall_memory(startdate, enddate)
