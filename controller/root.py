#!/usr/bin/env python3
'''Funtions for handling rest requests
    and root pages'''

import cherrypy
import html
from datetime import datetime
import re
from model import root
from controller.html import Html
from controller.memcache import Client as MClient
from jinja2 import Environment, FileSystemLoader


class Root(object):
    '''Funtions for handling rest requests
    and root pages'''

    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('views'))

    @cherrypy.expose
    def index(self):
        '''Build the index page
        and return html
        @return: html string
        @rtype: str'''
        index_html = self.env.get_template('index.html')
        nav = Html.get_navigation()
        return index_html.render(
            {'title': 'Home', 'nav': nav}
            )

    @cherrypy.expose
    def detail(self):
        '''Build the detail page
        and return html
        @return: html string
        @rtype: str'''
        index_html = self.env.get_template('detail.html')

        nav = Html.get_navigation('detail')
        return index_html.render(
            {'title': 'Detailed Statistics', 'nav': nav}
            )

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def first(self):
        '''Returns first server in
        the database
        @return: json string
        @rtype: dic'''
        return root.Root.get_first()

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def stats(self, server):
        '''Generate html for general status
        @return: json string
        @rtype: dic'''

        stats = []
        server = root.Root.get_server(server)

        if server.strip():
            mem_client = MClient([server])
            stats = mem_client.get_stats()
            mem_client.disconnect_all()

        output_html = []
        online_status = False
        if len(stats) > 0:
            stats = stats[0][1]

            stats_html = self.env.get_template('detail/stats.html')

            # Memcache current size in bytes
            p_bytes = int(stats['bytes'])
            # Memcache maximum size in bytes
            p_maxbytes = int(stats['limit_maxbytes'])
            # Convert to percentage
            p_percentage = round((p_bytes/p_maxbytes)*100, 2)

            progress_color = 'progress-bar-success'

            if p_percentage > 90:
                progress_color = 'progress-bar-warning'
            elif p_percentage > 80:
                progress_color = 'progress-bar-danger'

            # Memcache successfull hits
            p_get_hits = int(stats['get_hits'])
            # Memcache total hits
            p_cmd_get = int(stats['cmd_get'])
            # set if the p_cmd_get value is 0 to 1
            # Because cannot devide 0 from 0
            p_cmd_get = p_cmd_get if (p_cmd_get > 0) else 1
            # Convert to percentage
            p_cmd_percentage = round((p_get_hits / p_cmd_get) * 100, 2)

            cmd_progress_color = 'progress-bar-success'

            if p_percentage < 90:
                cmd_progress_color = 'progress-bar-warning'
            elif p_percentage < 80:
                cmd_progress_color = 'progress-bar-danger'

            server_time = datetime.fromtimestamp(int(stats['time']))

            stats_data = {'total_connections': stats['total_connections'],
                          'uptime': int(int(stats['uptime'])/(60 * 60 * 24)),
                          'server_time': server_time.strftime('%H:%M:%S'),
                          'curr_items': stats['curr_items'],
                          'cas_hits': stats['cas_hits'],
                          'cas_misses': stats['cas_misses'],
                          'cmd_get': stats['cmd_get'],
                          'cmd_set': stats['cmd_set'],
                          'storage_now': round(p_bytes/(1024*1024), 2),
                          'storage_max': round(p_maxbytes/(1024*1024), 2),
                          'storage_percentage': p_percentage,
                          'storage_color': progress_color,
                          'commands_now': p_cmd_get,
                          'commands_max': p_get_hits,
                          'commands_percentage': p_cmd_percentage,
                          'command_color': cmd_progress_color}
            output_html.append(stats_html.render(stats_data))
            online_status = True
        else:
            output_html.append('<div class="alert alert-danger" '
                               'role="alert">Could not retrive '
                               'infomation, server is offline</div>')

        return { 'html' : ''.join(output_html), 'online' : online_status }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def statst(self, server):
        '''Returns genaral stats for the provided server
        by server parameter
        @return: html table
        @rtype: str'''

        stats = []
        server = root.Root.get_server(server)

        if server.strip():
            mem_client = MClient([server])
            stats = mem_client.get_stats()
            mem_client.disconnect_all()

        t_rows = []

        if len(stats) > 0:
            for key, value in stats[0][1].items():
                t_rows.append((key, value))

        return t_rows

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def slabs(self, server):
        '''Returns html table of information
        about each of the slabs created by memcached during runtime
        @return: html table.
        @rtype: str'''

        stats = []
        server = root.Root.get_server(server)

        if server.strip():
            mem_client = MClient([server])

            # get slabs stats
            stats = mem_client.get_stats(stat_args="slabs")
            mem_client.disconnect_all()

        t_rows = []

        if len(stats) > 0:
            for key, value in stats[0][1].items():
                t_rows.append((key, value))

        return t_rows

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def sizes(self, server):
        ''' Returns html table of information about the
            general size and count of all items stored in the cache.

            Note: according the documentation when execute this command
            it will lockdown memcache server. so better make it optional
            for interface

            @return: html table
            @rtype: str
        '''

        stats = []
        server = root.Root.get_server(server)

        if server.strip():
            mem_client = MClient([server])

            # get all item stats
            stats = mem_client.get_stats(stat_args="sizes")
            mem_client.disconnect_all()

        t_rows = []

        if len(stats) > 0:
            for key, value in stats[0][1].items():
                t_rows.append((key, value))

        return t_rows

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def items(self, server):
        '''Returns html table of information about
        item storage per slab class.
        @return: html table
        @rtype: str'''

        stats = []
        server = root.Root.get_server(server)
        if server.strip():
            mem_client = MClient([server])

            # get all items stats
            stats = mem_client.get_stats(stat_args="items")
            mem_client.disconnect_all()

        t_rows = []

        if len(stats) > 0:
            for key, value in stats[0][1].items():
                t_rows.append((key, value))

        return t_rows

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def settings(self, server):
        '''Returns html table of details of
        the settings of the running memcached.
        @return: html table
        @rtype: str'''

        stats = []
        server = root.Root.get_server(server)
        if server.strip():
            mem_client = MClient([server])

            # get all details of settings
            stats = mem_client.get_stats(stat_args="settings")
            mem_client.disconnect_all()
            
        t_rows = []

        if len(stats) > 0:
            for key, value in stats[0][1].items():
                t_rows.append((key, value))

        return t_rows

    @cherrypy.expose
    def servers(self):
        '''Returns html list elements of servers
        @return: html table
        @rtype: str'''

        # get list of servers from sqlite database
        d_servers = root.Root.get_servers_weight()

        mem_client = MClient(d_servers)
        s_stats = mem_client.get_stats()
        mem_client.disconnect_all()

        online_servers = []

        pattern_obj = re.compile('\\s\\(\\d\\)')
        for server in s_stats:
            server_name = server[0].decode(encoding="utf-8")
            server_name = pattern_obj.sub('', server_name)
            online_servers.append(server_name)

        stats_html = self.env.get_template('detail/sidebar.html')
        render_data = {'online_servers': online_servers,
                       'servers': root.Root.get_servers()}
        return stats_html.render(render_data)

    @cherrypy.expose
    def onlinservers(self):
        '''Returns html for display onlin status
        about the servers.
        @return: html table
        @rtype: str'''

        s_servers = root.Root.get_servers_weight()

        mem_client = MClient(s_servers)
        s_stats = mem_client.get_stats()
        mem_client.disconnect_all()

        online_servers = []

        output_html = []
        pattern_obj = re.compile('\\s\\(\\d\\)')
        for server in s_stats:
            server_name = server[0].decode(encoding="ascii")
            server_name = pattern_obj.sub('', server_name)
            online_servers.append(server_name)

        online_html = self.env.get_template('home/online.html')

        render_dta = {'online_servers': online_servers,
                      'servers': s_servers}
        return online_html.render(render_dta)

    def gen_overall_html(self, overall):
        '''Returns html for overall status of
        the front page
        @return: html string
        @rtype: str'''

        output_html = []
        # Start bootstrap html row

        progress_color = 'progress-bar-success'

        if overall['spercentage'] > 90:
            progress_color = 'progress-bar-warning'
        elif overall['spercentage'] > 80:
            progress_color = 'progress-bar-danger'

        cmd_progress_color = 'progress-bar-success'

        if overall['cpercentage'] < 90:
            cmd_progress_color = 'progress-bar-warning'
        elif overall['cpercentage'] < 80:
            cmd_progress_color = 'progress-bar-danger'

        stats_html = self.env.get_template('home/stats.html')
        stats_data = {'total_connections': overall['connections'],
                      'curconnections': overall['curconnections'],
                      'items': overall['items'],
                      'curr_items': overall['items'],
                      'evictions': overall['evictions'],
                      'cashits': overall['cashits'],
                      'casmisses': overall['casmisses'],
                      'get': overall['get'],
                      'set': overall['set'],
                      'storage_now': overall['bytes'],
                      'storage_max': overall['maxbytes'],
                      'storage_percentage': overall['spercentage'],
                      'storage_color': progress_color,
                      'commands_now': overall['get'],
                      'commands_max': overall['gethits'],
                      'commands_percentage': overall['cpercentage'],
                      'command_color': cmd_progress_color}
        output_html.append(stats_html.render(stats_data))

        return ''.join(output_html)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def service(self):
        '''Returns json for display front page
        status
        @return: json string
        @rtype: str'''

        s_stats = []

        s_servers = root.Root.get_servers_weight()

        if s_servers:
            mem_client = MClient(s_servers)
            s_stats = mem_client.get_stats()
            mem_client.disconnect_all()

        data = []
        overall = {'items': 0, 'connections': 0, 'curconnections': 0,
                   'bytes': 0, 'maxbytes': 0, 'spercentage': 0,
                   'cpercentage': 0, 'cashits': 0, 'casmisses': 0,
                   'get': 0, 'set': 0, 'gethits': 0, 'evictions': 0}
        local = {'items': 0, 'connections': 0, 'curconnections': 0,
                 'bytes': 0, 'maxbytes': 0, 'spercentage': 0,
                 'cpercentage': 0, 'cashits': 0, 'casmisses': 0,
                 'get': 0, 'set': 0, 'gethits': 0, 'evictions': 0}

        pattern_obj = re.compile('\\s\\(\\d\\)')
        for server in s_stats:
            server_name = server[0].decode(encoding="ascii")
            server_name = pattern_obj.sub('', server_name)
            i_data = []
            # First index is the server address
            i_data.append(server_name)

            s_object = server[1]

            local['connections'] = int(s_object['total_connections'])
            local['curconnections'] = int(s_object['curr_connections'])
            local['items'] = int(s_object['total_items'])
            # Memcache current size in bytes
            local['bytes'] = int(s_object['bytes'])
            # Memcache maximum size in bytes
            local['maxbytes'] = int(s_object['limit_maxbytes'])
            local['evictions'] = int(s_object['evictions'])

            # Overall status
            overall['connections'] += local['connections']
            overall['curconnections'] += local['curconnections']
            overall['items'] += local['items']
            overall['bytes'] += local['bytes']
            overall['maxbytes'] += local['maxbytes']
            overall['gethits'] += int(s_object['get_hits'])
            overall['cashits'] += int(s_object['cas_hits'])
            overall['casmisses'] += int(s_object['cas_misses'])
            overall['get'] += int(s_object['cmd_get'])
            overall['set'] += int(s_object['cmd_set'])
            overall['evictions'] += int(s_object['evictions'])

            free_storage = (local['maxbytes'] - local['bytes'])/(1024*1024)

            i_data.append(s_object['version'])
            i_data.append(local['items'])
            t_time = datetime.fromtimestamp(int(s_object['time']))
            i_data.append(t_time.strftime('%Y-%m-%d %H:%M:%S'))
            i_data.append(int(int(s_object['uptime'])/(60 * 60 * 24)))
            i_data.append(local['connections'])
            i_data.append(local['curconnections'])
            i_data.append(round(free_storage, 2))
            i_data.append(local['evictions'])
            data.append(i_data)

        # Convert to percentage
        if overall['maxbytes'] <= 1:  # Fix division by zero
            overall['spercentage'] = (overall['bytes']/1)*100
        else:
            storage_percentage = (overall['bytes']/overall['maxbytes'])*100
            overall['spercentage'] = round(storage_percentage, 2)

        overall['get'] = overall['get'] if (overall['get'] > 0) else 1

        # Convert to percentage
        if overall['get'] <= 1:  # Fix division by zero
            overall['cpercentage'] = (overall['gethits'] / 1) * 100
        else:
            hit_ratio = (overall['gethits'] / overall['get']) * 100
            overall['cpercentage'] = round(hit_ratio, 2)

        overall['bytes'] = round(overall['bytes']/(1024*1024), 2)
        overall['maxbytes'] = round(overall['maxbytes']/(1024*1024), 2)

        return {'data': data, 'overall': self.gen_overall_html(overall)}
