
import MySQLdb
from .mdatabase import MDatabase
from datetime import datetime
from cherrypy import log

T_FORMAT = "%y-%m-%d (%I:%M %p)"

class Graph(object):

    @staticmethod
    def get_hitsgraph(sid, startdate, enddate):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        hits = []
        misses = []
        
        d1 = datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.strptime(enddate, '%Y-%m-%d %H:%M:%S')

        hour_diff = abs(d2-d1).total_seconds() / 3600.0
        
        sql_query = 'SELECT `get_hits`, `get_misses`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s ORDER BY record ASC'
        
        log.error('{}'.format(hour_diff))
        
        if hour_diff > 24:
            sql_query = 'SELECT `get_hits`, `get_misses`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s GROUP BY HOUR(record) ORDER BY record ASC'
        elif hour_diff > 5:
            sql_query = 'SELECT `get_hits`, `get_misses`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s GROUP BY ROUND(UNIX_TIMESTAMP(record)/(10 * 60)) ORDER BY record ASC'

        with MDatabase.connect() as con:
            con.execute(sql_query, (sid, startdate, enddate))            
            for server in con.fetchall():
                hits.append(server[0])
                misses.append(server[1])
                labels.append(server[2].strftime(T_FORMAT))
                
        datasets.append({'data' : hits,
                         'label': 'Hits',
                         'fillColor' : 'rgba(99, 123, 133, 0.1)',
                         'strokeColor' : '#637b85',
                         'pointColor' : '#637b85)',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#637b85',
                         'pointHighlightStroke' : '#ffffff'
                        })
        datasets.append({'data' : misses,
                         'label': 'Misses',
                         'fillColor' : 'rgba(44, 156, 105, 0.1)',
                         'strokeColor' : '#2c9c69',
                         'pointColor' : '#2c9c69',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#2c9c69',
                         'pointHighlightStroke' : '#ffffff'
                        })
        return {'datasets' : datasets, 'labels' : labels}
    
    @staticmethod
    def get_cmdgraph(sid, startdate, enddate):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        setcmd = []
        getcmd = []
        
        d1 = datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.strptime(enddate, '%Y-%m-%d %H:%M:%S')

        hour_diff = abs(d2-d1).total_seconds() / 3600.0
        
        sql_query = 'SELECT `set_cmd`, `get_cmd`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s ORDER BY record ASC'
        
        if hour_diff > 24:
            sql_query = 'SELECT `set_cmd`, `get_cmd`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s GROUP BY HOUR(record) ORDER BY record ASC'
        elif hour_diff > 5:
            sql_query = 'SELECT `set_cmd`, `get_cmd`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s GROUP BY ROUND(UNIX_TIMESTAMP(record)/(10 * 60)) ORDER BY record ASC'

        
        with MDatabase.connect() as con:
            con.execute(sql_query, (sid, startdate, enddate))
            for server in con.fetchall():
                setcmd.append(server[0])
                getcmd.append(server[1])
                labels.append(server[2].strftime(T_FORMAT))
                
        datasets.append({'data' : setcmd,
                         'label': 'Set',
                         'fillColor' : 'rgba(244, 203, 61, 0.1)',
                         'strokeColor' : '#f4cb3d',
                         'pointColor' : '#f4cb3d',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#f4cb3d',
                         'pointHighlightStroke' : '#ffffff'
                        })
        datasets.append({'data' : getcmd,
                         'label': 'Get',
                         'fillColor' : 'rgba(205, 118, 23, 0.1)',
                         'strokeColor' : '#cd7617',
                         'pointColor' : '#cd7617',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#cd7617',
                         'pointHighlightStroke' : '#ffffff'
                        })
        return {'datasets' : datasets, 'labels' : labels}
    
    @staticmethod
    def get_cacheditems(sid, startdate, enddate):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        cached_items = []
        
        d1 = datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.strptime(enddate, '%Y-%m-%d %H:%M:%S')

        hour_diff = abs(d2-d1).total_seconds() / 3600.0
        
        sql_query = 'SELECT `cached_items`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s ORDER BY record ASC'
        
        if hour_diff > 24:
            sql_query = 'SELECT `cached_items`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s GROUP BY HOUR(record) ORDER BY record ASC'
        elif hour_diff > 5:
            sql_query = 'SELECT `cached_items`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s GROUP BY ROUND(UNIX_TIMESTAMP(record)/(10 * 60)) ORDER BY record ASC'

        
        with MDatabase.connect() as con:
            con.execute(sql_query, (sid, startdate, enddate))            
            for server in con.fetchall():
                cached_items.append(server[0])
                labels.append(server[1].strftime(T_FORMAT))
                
        datasets.append({'data' : cached_items,
                         'label': 'Cached Items',
                         'fillColor' : 'rgba(30, 141, 171, 0.1)',
                         'strokeColor' : '#1E8DAB',
                         'pointColor' : '#1E8DAB',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#1E8DAB',
                         'pointHighlightStroke' : '#ffffff'
                        })
        return {'datasets' : datasets, 'labels' : labels}
    
    @staticmethod
    def get_memory(sid, startdate, enddate):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        memory = []
        
        d1 = datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.strptime(enddate, '%Y-%m-%d %H:%M:%S')

        hour_diff = abs(d2-d1).total_seconds() / 3600.0
        
        sql_query = 'SELECT `memory`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s ORDER BY record ASC'
        
        if hour_diff > 24:
            sql_query = 'SELECT `memory`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s GROUP BY HOUR(record) ORDER BY record ASC'
        elif hour_diff > 5:
            sql_query = 'SELECT `memory`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s GROUP BY ROUND(UNIX_TIMESTAMP(record)/(10 * 60)) ORDER BY record ASC'

        
        with MDatabase.connect() as con:
            con.execute(sql_query, (sid, startdate, enddate))          
            for server in con.fetchall():
                memory.append(server[0])
                labels.append(server[1].strftime(T_FORMAT))
                
        datasets.append({'data' : memory,
                         'label': 'Memory',
                         'fillColor' : 'rgba(128, 72, 1, 0.1)',
                         'strokeColor' : '#804801',
                         'pointColor' : '#804801',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#804801',
                         'pointHighlightStroke' : '#ffffff'
                        })
        return {'datasets' : datasets, 'labels' : labels}

    @staticmethod
    def get_responsetime(sid, startdate, enddate):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        response_time = []
        
        d1 = datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.strptime(enddate, '%Y-%m-%d %H:%M:%S')

        hour_diff = abs(d2-d1).total_seconds() / 3600.0
        
        sql_query = 'SELECT `response_time`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s ORDER BY record ASC'
        
        if hour_diff > 24:
            sql_query = 'SELECT `response_time`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s GROUP BY HOUR(record) ORDER BY record ASC'
        elif hour_diff > 5:
            sql_query = 'SELECT `response_time`, `record` FROM statistics WHERE server_id=%s AND record BETWEEN %s AND %s GROUP BY ROUND(UNIX_TIMESTAMP(record)/(10 * 60)) ORDER BY record ASC'

        
        with MDatabase.connect() as con:
            con.execute(sql_query, (sid, startdate, enddate))          
            for server in con.fetchall():
                response_time.append(server[0])
                labels.append(server[1].strftime(T_FORMAT))
                
        datasets.append({'data' : response_time,
                         'label': 'Response Time',
                         'fillColor' : 'rgba(232, 107, 88, 0.1)',
                         'strokeColor' : '#E86B58',
                         'pointColor' : '#E86B58',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#E86B58',
                         'pointHighlightStroke' : '#ffffff'
                        })
        return {'datasets' : datasets, 'labels' : labels}

    @staticmethod
    def overall_hitsgraph(startdate, enddate):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        hits = []
        misses = []
        
        d1 = datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.strptime(enddate, '%Y-%m-%d %H:%M:%S')

        hour_diff = abs(d2-d1).total_seconds() / 3600.0
        
        sql_query = 'SELECT sum(`get_hits`), sum(`get_misses`), `record` FROM statistics WHERE record BETWEEN %s AND %s GROUP BY record ORDER BY record ASC'
        
        if hour_diff > 24:
            sql_query = 'SELECT sum(`get_hits`), sum(`get_misses`), `record` FROM statistics WHERE record BETWEEN %s AND %s GROUP BY HOUR(record) ORDER BY record ASC'
        elif hour_diff > 5:
            sql_query = 'SELECT sum(`get_hits`), sum(`get_misses`), `record` FROM statistics WHERE record BETWEEN %s AND %s GROUP BY ROUND(UNIX_TIMESTAMP(record)/(10 * 60)) ORDER BY record ASC'

        with MDatabase.connect() as con:
            con.execute(sql_query, (startdate, enddate))
            for server in con.fetchall():
                hits.append(server[0])
                misses.append(server[1])
                labels.append(server[2].strftime(T_FORMAT))
                
        datasets.append({'data' : hits,
                         'label': 'Hits',
                         'fillColor' : 'rgba(99, 123, 133, 0.1)',
                         'strokeColor' : '#637b85',
                         'pointColor' : '#637b85',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#637b85',
                         'pointHighlightStroke' : '#ffffff'
                        })
        datasets.append({'data' : misses,
                         'label': 'Misses',
                         'fillColor' : 'rgba(44, 156, 105, 0.1)',
                         'strokeColor' : '#2c9c69',
                         'pointColor' : '#2c9c69',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#2c9c69',
                         'pointHighlightStroke' : '#ffffff'
                        })
        return {'datasets' : datasets, 'labels' : labels}
    
    @staticmethod
    def overall_cmdgraph(startdate, enddate):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        setcmd = []
        getcmd = []
        
        d1 = datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.strptime(enddate, '%Y-%m-%d %H:%M:%S')

        hour_diff = abs(d2-d1).total_seconds() / 3600.0
        
        sql_query = 'SELECT sum(`set_cmd`), sum(`get_cmd`), `record` FROM statistics WHERE record BETWEEN %s AND %s GROUP BY record ORDER BY record ASC'
        
        if hour_diff > 24:
            sql_query = 'SELECT sum(`set_cmd`), sum(`get_cmd`), `record` FROM statistics WHERE record BETWEEN %s AND %s GROUP BY HOUR(record) ORDER BY record ASC'
        elif hour_diff > 5:
            sql_query = 'SELECT sum(`set_cmd`), sum(`get_cmd`), `record` FROM statistics WHERE record BETWEEN %s AND %s GROUP BY ROUND(UNIX_TIMESTAMP(record)/(10 * 60)) ORDER BY record ASC'

        with MDatabase.connect() as con:
            con.execute(sql_query, (startdate, enddate)) 
            for server in con.fetchall():
                setcmd.append(server[0])
                getcmd.append(server[1])
                labels.append(server[2].strftime(T_FORMAT))
                
        datasets.append({'data' : setcmd,
                         'label': 'Set',
                         'fillColor' : 'rgba(244, 203, 61, 0.1)',
                         'strokeColor' : '#f4cb3d',
                         'pointColor' : '#f4cb3d',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#f4cb3d',
                         'pointHighlightStroke' : '#ffffff'
                        })
        datasets.append({'data' : getcmd,
                         'label': 'Get',
                         'fillColor' : 'rgba(205, 118, 23, 0.1)',
                         'strokeColor' : '#cd7617',
                         'pointColor' : '#cd7617',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#cd7617',
                         'pointHighlightStroke' : '#ffffff'
                        })
        return {'datasets' : datasets, 'labels' : labels}
    
    @staticmethod
    def overall_cacheditems(startdate, enddate):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        cached_items = []
        
        d1 = datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.strptime(enddate, '%Y-%m-%d %H:%M:%S')

        hour_diff = abs(d2-d1).total_seconds() / 3600.0
        
        sql_query = 'SELECT sum(`cached_items`), `record` FROM statistics WHERE record BETWEEN %s AND %s GROUP BY record ORDER BY record ASC'
        
        if hour_diff > 5:
            sql_query = 'SELECT sum(`cached_items`), `record` FROM statistics WHERE record BETWEEN %s AND %s GROUP BY HOUR(record) ORDER BY record ASC'
        elif hour_diff > 5:
            sql_query = 'SELECT sum(`cached_items`), `record` FROM statistics WHERE record BETWEEN %s AND %s GROUP BY ROUND(UNIX_TIMESTAMP(record)/(10 * 60)) ORDER BY record ASC'

        
        with MDatabase.connect() as con:
            con.execute(sql_query, (startdate, enddate))       
            for server in con.fetchall():
                cached_items.append(server[0])
                labels.append(server[1].strftime(T_FORMAT))
                
        datasets.append({'data' : cached_items,
                         'label': 'Cached Items',
                         'fillColor' : 'rgba(30, 141, 171, 0.1)',
                         'strokeColor' : '#1E8DAB',
                         'pointColor' : '#1E8DAB',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#1E8DAB',
                         'pointHighlightStroke' : '#ffffff'
                        })
        return {'datasets' : datasets, 'labels' : labels}
    
    @staticmethod
    def overall_memory(startdate, enddate):
        '''Return list of list get hits and misses'''
        
        datasets = []
        labels = []
        
        memory = []
        
        d1 = datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.strptime(enddate, '%Y-%m-%d %H:%M:%S')

        hour_diff = abs(d2-d1).total_seconds() / 3600.0
        
        sql_query = 'SELECT sum(`memory`), `record` FROM statistics WHERE record BETWEEN %s AND %s GROUP BY record ORDER BY record ASC'
        
        if hour_diff > 24:
            sql_query = 'SELECT sum(`memory`), `record` FROM statistics WHERE record BETWEEN %s AND %s GROUP BY HOUR(record) ORDER BY record ASC'
        elif hour_diff > 5:
            sql_query = 'SELECT sum(`memory`), `record` FROM statistics WHERE record BETWEEN %s AND %s GROUP BY ROUND(UNIX_TIMESTAMP(record)/(10 * 60)) ORDER BY record ASC'

        
        with MDatabase.connect() as con:
            con.execute(sql_query, (startdate, enddate))        
            for server in con.fetchall():
                memory.append(server[0])
                labels.append(server[1].strftime(T_FORMAT))
                
        datasets.append({'data' : memory,
                         'label': 'Memory',
                         'fillColor' : 'rgba(128, 72, 1, 0.1)',
                         'strokeColor' : '#804801',
                         'pointColor' : '#804801',
                         'pointStrokeColor' : '#ffffff',
                         'pointHighlightFill' : '#804801',
                         'pointHighlightStroke' : '#ffffff'
                        })
        return {'datasets' : datasets, 'labels' : labels}

    @staticmethod
    def insert_statistic(sid, stats):
        '''Insert new row to stats table'''
        rowid = 0
        sql_query = 'INSERT INTO statistics(`server_id`, `get_hits`, `get_misses`, `set_cmd`, `get_cmd`, `cached_items`, `response_time`, `memory`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        with MDatabase.connect() as con:
            con.execute(sql_query, (sid, stats['get_hits'], stats['get_misses'], stats['cmd_set'], stats['cmd_get'], stats['curr_items'], stats['response_time'], stats['bytes']))
            rowid = con.lastrowid
        return rowid