from .mdatabase import MDatabase

class Admin(object):

    @staticmethod
    def insert_server(name, port):
        '''Insert new row to server table'''
        rowid = 0
        sql_query = 'INSERT INTO servers(`name`, `port`) VALUES (%s, %s)'
        with MDatabase.connect() as con:
            con.execute(sql_query, (name.strip(), port.strip()))
            rowid = con.lastrowid
        return rowid

    @staticmethod
    def update_server(name, port, sid):
        '''Update existing row in server table'''
        affected_rows = 0
        sql_query = 'UPDATE servers SET name=%s, port=%s WHERE id=%s'        
        with MDatabase.connect() as con:
            con.execute(sql_query, (name.strip(), port.strip(), sid.strip()))
            affected_rows = con.rowcount
        return True if affected_rows > 0 else False

    @staticmethod
    def delete_server(sid):
        '''Delete existing row in server table'''
        affected_rows = 0
        sql_query = 'DELETE from servers where id=%s'
        with MDatabase.connect() as con:
            con.execute(sql_query, (sid.strip()))
            affected_rows = con.rowcount
        return True if affected_rows > 0 else False
    
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