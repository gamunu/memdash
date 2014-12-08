
import MySQLdb
from .mdatabase import MDatabase

class Graph(object):

    @staticmethod
    def get_hitsgraph(sid):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        hits = []
        misses = []
        sql_query = 'SELECT * FROM (SELECT `get_hits`, `get_misses`, `record` FROM statistics WHERE server_id=%s ORDER BY record DESC LIMIT 20) t ORDER BY t.record ASC'
        with MDatabase.connect() as con:
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
    
    @staticmethod
    def get_cmdgraph(sid):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        setcmd = []
        getcmd = []
        sql_query = 'SELECT * FROM (SELECT `set_cmd`, `get_cmd`, `record` FROM statistics WHERE server_id=%s ORDER BY record DESC LIMIT 20) t ORDER BY t.record ASC'
        with MDatabase.connect() as con:
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
    
    @staticmethod
    def get_cacheditems(sid):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        cached_items = []
        sql_query = 'SELECT * FROM (SELECT `cached_items`, `record` FROM statistics WHERE server_id=%s ORDER BY record DESC LIMIT 20) t ORDER BY t.record ASC'
        with MDatabase.connect() as con:
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
    
    @staticmethod
    def get_memory(sid):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        memory = []
        sql_query = 'SELECT * FROM (SELECT `memory`, `record` FROM statistics WHERE server_id=%s ORDER BY record DESC LIMIT 20) t ORDER BY t.record ASC'
        with MDatabase.connect() as con:
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

    @staticmethod
    def insert_statistic(sid, stats):
        '''Insert new row to stats table'''
        rowid = 0
        sql_query = 'INSERT INTO statistics(`server_id`, `get_hits`, `get_misses`, `set_cmd`, `get_cmd`, `cached_items`, `responce_time`, `memory`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        with self.connect() as con:
            con.execute(sql_query, (sid, stats['get_hits'], stats['get_misses'], stats['cmd_set'], stats['cmd_get'], stats['curr_items'], stats['response_time'], stats['bytes']))
            rowid = con.lastrowid
        return rowid