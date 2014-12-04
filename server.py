'''Main server entre'''

import os, os.path
import cherrypy
from lib import mdatabase, root, admin, graph, daemon

def main():
    '''Main server entre'''
    cherrypy.config.update({'server.socket_port' : 8090})

    conf = {
        '/' : {
            'tools.sessions.on': False,
            'tools.caching.on': True,
            'tools.expires.on': True,
            'tools.expires.secs': 2592000,
            'tools.gzip.mime_types': ['text/*'],
            'tools.gzip.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static' : {
            'tools.staticdir.on': True,
            'tools.gzip.mime_types': ['text/*'],
            'tools.gzip.on': True,
            'tools.staticdir.content_types': {
                'woff': 'application/font-woff'
                },
            'tools.staticdir.dir': './public'
        }
    }

    database = mdatabase.MDatabase('memdash','root','mariadb')

    #Do not uncomment this will whipe whole database
    #cherrypy.engine.subscribe('stop', db.cleanup_database)

    page = root.Root(database)
    page.admin = admin.Admin(database)
    page.graph = graph.Graph(database)

    thread1 = daemon.Daemon(database)
    thread1.start()
    
    cherrypy.quickstart(page, '/', conf)

if __name__ == '__main__':
    main()
