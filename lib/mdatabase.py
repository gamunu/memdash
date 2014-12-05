#!/usr/bin/env python3
'''Database handling functions'''

import MySQLdb

class MDatabase(object):
    '''Database handling functions'''

    def __init__(self, dbname, dbuser, dbpass):
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpass = dbpass
        
    def connect(self):
        return MySQLdb.Connection(user=self.dbuser, passwd=self.dbpass, db=self.dbname)

    def insert_server(self, name, port):
        '''Insert new row to server table'''
        rowid = 0
        sql_query = 'INSERT INTO servers(`name`, `port`) VALUES (%s, %s)'
        with self.connect() as con:
            con.execute(sql_query, (name.strip(), port.strip()))
            rowid = con.lastrowid
        return rowid

    def update_server(self, name, port, sid):
        '''Update existing row in server table'''
        affected_rows = 0
        sql_query = 'UPDATE servers SET name=%s, port=%s WHERE id=%s'        
        with self.connect() as con:
            con.execute(sql_query, (name.strip(), port.strip(), sid.strip()))
            affected_rows = con.rowcount
        return True if affected_rows > 0 else False

    def delete_server(self, sid):
        '''Delete existing row in server table'''
        affected_rows = 0
        sql_query = 'DELETE from servers where id=%s'
        with self.connect() as con:
            con.execute(sql_query, (sid.strip()))
            affected_rows = con.rowcount
        return True if affected_rows > 0 else False

    def get_servers_weight(self):
        '''Return list of tuples with server name, port
        and weight for each server to use in
        memchache library'''
        server_list = []
        sql_query = 'SELECT name, port FROM servers ORDER BY id ASC'
        with self.connect() as con:
            weight = 0
            con.execute(sql_query)
            for server in con.fetchall():
                weight = weight + 1
                address = '{}:{}'.format(server[0], server[1])
                server_list.append((address, weight))
        return server_list
    
    def get_servers(self):
        '''Return list of tuples with server name, port
        and weight for each server to use in
        memchache library'''
        server_list = []
        sql_query = 'SELECT id, name, port FROM servers ORDER BY id ASC'
        with self.connect() as con:
            con.execute(sql_query)
            for server in con.fetchall():
                address = '{}:{}'.format(server[1], server[2])
                server_list.append((address, server[0]))
        return server_list

    def get_server_list(self):
        '''Return list of dictionary with server name, port'''
        server_list = []
        sql_query = 'SELECT * FROM servers ORDER BY id ASC'
        with self.connect() as con:
            con.execute(sql_query)
            for server in con.fetchall():
                address = {}
                address['id'] = server[0]
                address['server'] = server[1]
                address['port'] = server[2]
                server_list.append(address)
        return server_list

    def get_server(self, sid):
        '''Get single server where server id equls to sid'''
        address = ''
        sql_query = 'SELECT * FROM servers WHERE id=%s'
        with self.connect() as con:
            con.execute(sql_query, (sid, ))
            server = con.fetchone()
            if server:
                address = '{}:{}'.format(server[1], server[2])
        return address
    
    def get_first(self):
        '''Return the first row servers table'''
        address = ''
        sid = 0
        sql_query = 'SELECT * FROM servers ORDER BY id ASC LIMIT 1'
        with self.connect() as con:
            con.execute(sql_query)
            server = con.fetchone()
            if server:
                address = '{}:{}'.format(server[1], server[2])
                sid = server[0]
        return {'address' : address, 'id' : sid}
    
    def get_hitsgraph(self, sid):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        hits = []
        misses = []
        sql_query = 'SELECT get_hits, get_misses, record FROM statistics WHERE server_id=%s ORDER BY record ASC LIMIT 8'
        with self.connect() as con:
            con.execute(sql_query, (sid, ))            
            for server in con.fetchall():
                hits.append(server[0])
                misses.append(server[1])
                labels.append(server[2].strftime("%H:%M:%S"))
                
        datasets.append({'data' : hits,
                         'label': 'Hits',
                         'fillColor' : '#637b85',
                         'strokeColor' : 'rgba(220,220,220,1)',
                         'pointColor' : 'rgba(220,220,220,1)',
                         'pointStrokeColor' : '#fff',
                         'pointHighlightFill' : '#fff',
                         'pointHighlightStroke' : 'rgba(220,220,220,1)'
                        })
        datasets.append({'data' : misses,
                         'label': 'Misses',
                         'fillColor' : '#2c9c69',
                         'strokeColor' : 'rgba(220,220,220,1)',
                         'pointColor' : 'rgba(220,220,220,1)',
                         'pointStrokeColor' : '#fff',
                         'pointHighlightFill' : '#fff',
                         'pointHighlightStroke' : 'rgba(220,220,220,1)'
                        })
        return {'datasets' : datasets, 'labels' : labels}
    
    def get_cmdgraph(self, sid):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        setcmd = []
        getcmd = []
        sql_query = 'SELECT set_cmd, get_cmd, record FROM statistics WHERE server_id=%s ORDER BY record ASC LIMIT 8'
        with self.connect() as con:
            con.execute(sql_query, (sid, ))            
            for server in con.fetchall():
                setcmd.append(server[0])
                getcmd.append(server[1])
                labels.append(server[2].strftime("%H:%M:%S"))
                
        datasets.append({'data' : setcmd,
                         'label': 'Set',
                         'fillColor' : '#F4CB3D',
                         'strokeColor' : 'rgba(220,220,220,1)',
                         'pointColor' : 'rgba(220,220,220,1)',
                         'pointStrokeColor' : '#fff',
                         'pointHighlightFill' : '#fff',
                         'pointHighlightStroke' : 'rgba(220,220,220,1)'
                        })
        datasets.append({'data' : getcmd,
                         'label': 'Get',
                         'fillColor' : '#CD7617',
                         'strokeColor' : 'rgba(220,220,220,1)',
                         'pointColor' : 'rgba(220,220,220,1)',
                         'pointStrokeColor' : '#fff',
                         'pointHighlightFill' : '#fff',
                         'pointHighlightStroke' : 'rgba(220,220,220,1)'
                        })
        return {'datasets' : datasets, 'labels' : labels}
    
    def get_cacheditems(self, sid):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        cached_items = []
        sql_query = 'SELECT cached_items, record FROM statistics WHERE server_id=%s ORDER BY record ASC LIMIT 8'
        with self.connect() as con:
            con.execute(sql_query, (sid, ))            
            for server in con.fetchall():
                cached_items.append(server[0])
                labels.append(server[1].strftime("%H:%M:%S"))
                
        datasets.append({'data' : cached_items,
                         'label': 'Cached Items',
                         'fillColor' : '#1E8DAB',
                         'strokeColor' : 'rgba(220,220,220,1)',
                         'pointColor' : 'rgba(220,220,220,1)',
                         'pointStrokeColor' : '#fff',
                         'pointHighlightFill' : '#fff',
                         'pointHighlightStroke' : 'rgba(220,220,220,1)'
                        })
        return {'datasets' : datasets, 'labels' : labels}
    
    def get_memory(self, sid):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        memory = []
        sql_query = 'SELECT memory, record FROM statistics WHERE server_id=%s ORDER BY record ASC LIMIT 8'
        with self.connect() as con:
            con.execute(sql_query, (sid, ))            
            for server in con.fetchall():
                memory.append(server[0])
                labels.append(server[1].strftime("%H:%M:%S"))
                
        datasets.append({'data' : memory,
                         'label': 'Memory',
                         'fillColor' : '#804801',
                         'strokeColor' : 'rgba(220,220,220,1)',
                         'pointColor' : 'rgba(220,220,220,1)',
                         'pointStrokeColor' : '#fff',
                         'pointHighlightFill' : '#fff',
                         'pointHighlightStroke' : 'rgba(220,220,220,1)'
                        })
        return {'datasets' : datasets, 'labels' : labels}

    def insert_statistic(self, sid, stats):
        '''Insert new row to stats table'''
        rowid = 0
        sql_query = 'INSERT INTO statistics(`server_id`, `get_hits`, `get_misses`, `set_cmd`, `get_cmd`, `cached_items`, `responce_time`, `memory`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        with self.connect() as con:
            con.execute(sql_query, (sid, stats['get_hits'], stats['get_misses'], stats['cmd_set'], stats['cmd_get'], stats['curr_items'], stats['response_time'], stats['bytes']))
            rowid = con.lastrowid
        return rowid