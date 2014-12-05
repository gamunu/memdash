#!/usr/bin/env python3
'''Background Daemon fetch data'''

from lib.memcache import Client as MClient
from timeit import Timer
import time


class Daemon(object):

    def __init__(self, db):
        ''' Constructor. '''
        self.database = db
        self.stats_current = {}
        self.stats_old = {}
        self.stats_new = {}

    def execute(self):
        ''' Run in the background '''
        for server in self.database.get_servers():
            print(server)
            if self.fetch(server[0], server[1]):
                if server[1] in self.stats_old:
                    self.extract_new(server[1])
                    self.insert_records()
                    self.stats_old[server[1]] = self.stats_current[server[1]]
                else:
                    self.stats_old[server[1]] = self.stats_current[server[1]]
                    self.fetch(server[0], server[1])

    def fetch(self, server, sid):
        '''Generate html for general status
        @return: json string
        @rtype: dic'''

        print("fetching from {} {}".format(server, sid))
        stats = []
        mem_client = MClient([server], debug=0)

        time_elapsed = 0
        timer = Timer(mem_client.get_stats)
        while True:
            try:
                stats = mem_client.get_stats()
                #Messure the response time
                time_elapsed = timer.timeit(1)
                mem_client.forget_dead_hosts()
            except Exception:
                mem_client = MClient([server], debug=0)
                continue
            break

        if len(stats) > 0:
            stats = stats[0][1]
            stats['response_time'] = time_elapsed
            self.stats_current[sid] = stats
            return True
        return False

    def extract_new(self, sid):
        '''Extract curretn values'''
        status_loc = {}
        print('Extracting {}'.format(sid))
        status_loc['get_hits'] = int(self.stats_current[sid]['get_hits']) - int(self.stats_old[sid]['get_hits'])
        status_loc['get_misses'] = int(self.stats_current[sid]['get_misses']) - int(self.stats_old[sid]['get_misses'])
        status_loc['cmd_get'] = int(self.stats_current[sid]['cmd_get']) - int(self.stats_old[sid]['cmd_get'])
        status_loc['cmd_set'] = int(self.stats_current[sid]['cmd_set']) - int(self.stats_old[sid]['cmd_set'])
        status_loc['curr_items'] = int(self.stats_current[sid]['curr_items'])
        status_loc['response_time'] = self.stats_current[sid]['response_time']
        status_loc['bytes'] = round(int(self.stats_current[sid]['bytes'])/(1024*1024), 2)
        
        self.stats_new[sid] = status_loc

    def insert_records(self):
        '''Insert data to database'''

        for stats in self.stats_new:
            s_stat = self.stats_new[stats]
            self.database.insert_statistic(stats, s_stat)
