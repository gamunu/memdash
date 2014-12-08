#!/usr/bin/env python3
"""
MemDash 1.0 Windows service.
Requires Mark Hammond's pywin32 package.
"""
import os
import os.path
import cherrypy
from controller import root, admin, graph, daemon
from config import Config
import win32serviceutil
import win32service
from cherrypy.process.plugins import Monitor


class MDashService(win32serviceutil.ServiceFramework):
    """MemDash NT Service."""

    _svc_name_ = "MemDash"
    _svc_display_name_ = "MemDash Service"

    def SvcDoRun(self):
        # Fix file paths,
        # chage directory to current working
        # directory'
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        conf = {
            '/': {
                'tools.gzip.mime_types': ['text/*'],
                'tools.gzip.on': True,
                'tools.staticdir.root': os.path.abspath(os.getcwd())
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.gzip.mime_types': ['text/*'],
                'tools.gzip.on': True,
                'tools.staticdir.content_types': {
                    'woff': 'application/font-woff'
                    },
                'tools.staticdir.dir': './public'
            }
        }

        # Do not uncomment this will whipe whole database
        # cherrypy.engine.subscribe('stop', db.cleanup_database)

        page = root.Root()
        page.admin = admin.Admin()
        page.graph = graph.Graph()

        cherrypy.tree.mount(page, '/', conf)

        # in practice, you will want to specify a value for
        # log.error_file below or in your config file.  If you
        # use a config file, be sure to use an absolute path to
        # it, as you can't be assured what path your service
        # will run in
        cherrypy.config.update({
            'global': {
                'server.socket_host': '0.0.0.0',
                'server.socket_port': 8989,
                'environment': 'embedded',
                'log.screen': False,
                'log.error_file': 'log.txt',
                'engine.autoreload.on': False,
                'engine.SIGHUP': None,
                'engine.SIGTERM': None,
                'response.headers.server': "MemDash v1.0",
                'tools.sessions.on': False,
                'tools.caching.on': False,
                'tools.expires.on': True,
                'tools.expires.secs': 2592000,
                }
            })

        c_daemon = daemon.Daemon()
        Monitor(cherrypy.engine, c_daemon.execute, frequency=Config.DE_FREQUENCY).subscribe()
        
        cherrypy.engine.start()
        cherrypy.engine.block()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        cherrypy.engine.exit()

        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        # very important for use with py2exe
        # otherwise the Service Controller never knows that it is stopped !

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MDashService)
