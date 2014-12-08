import MySQLdb
from .mdatabase import MDatabase

class Root(object):

    @staticmethod
    def get_servers_weight():
        '''Return list of tuples with server name, port
        and weight for each server to use in
        memchache library'''
        server_list = []
        sql_query = 'SELECT name, port FROM servers ORDER BY id ASC'
        with MDatabase.connect() as con:
            weight = 0
            con.execute(sql_query)
            for server in con.fetchall():
                weight = weight + 1
                address = '{}:{}'.format(server[0], server[1])
                server_list.append((address, weight))
        return server_list

    @staticmethod
    def get_servers():
        '''Return list of tuples with server name, port
        and weight for each server to use in
        memchache library'''
        server_list = []
        sql_query = 'SELECT id, name, port FROM servers ORDER BY id ASC'
        with MDatabase.connect() as con:
            con.execute(sql_query)
            for server in con.fetchall():
                address = '{}:{}'.format(server[1], server[2])
                server_list.append((address, server[0]))
        return server_list

    @staticmethod
    def get_server_list():
        '''Return list of dictionary with server name, port'''
        server_list = []
        sql_query = 'SELECT * FROM servers ORDER BY id ASC'
        with MDatabase.connect() as con:
            con.execute(sql_query)
            for server in con.fetchall():
                address = {}
                address['id'] = server[0]
                address['server'] = server[1]
                address['port'] = server[2]
                server_list.append(address)
        return server_list

    @staticmethod
    def get_server(sid):
        '''Get single server where server id equls to sid'''
        address = ''
        sql_query = 'SELECT * FROM servers WHERE id=%s'
        with MDatabase.connect() as con:
            con.execute(sql_query, (sid, ))
            server = con.fetchone()
            if server:
                address = '{}:{}'.format(server[1], server[2])
        return address

    @staticmethod
    def get_first():
        '''Return the first row servers table'''
        address = ''
        sid = 0
        sql_query = 'SELECT * FROM servers ORDER BY id ASC LIMIT 1'
        with MDatabase.connect() as con:
            con.execute(sql_query)
            server = con.fetchone()
            if server:
                address = '{}:{}'.format(server[1], server[2])
                sid = server[0]
        return {'address' : address, 'id' : sid}
