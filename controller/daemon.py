#!/usr/bin/env python3
'''Background Daemon fetch data'''

import controller
from timeit import Timer
from model.mdatabase import MDatabase
import time


class Daemon(object):

    def __init__(self):
        ''' Constructor. '''

        self.stats_current = {}
        self.stats_old = {}
        self.stats_new = {}

    def execute(self):
        ''' Run in the background '''
        for server in MDatabase.get_servers():
            print(server)
            if self.fetch(server[0], server[1]):
                if server[1] in self.stats_old:
                    self.extract_new(server[1])
                    self.stats_old[server[1]] = self.stats_current[server[1]]
                else:
                    self.stats_old[server[1]] = self.stats_current[server[1]]
                    self.fetch(server[0], server[1])
        self.insert_records()

    def fetch(self, server, sid):
        '''Generate html for general status
        @return: json string
        @rtype: dic'''

        print("fetching from {} {}".format(server, sid))
        stats = []
        mem_client = MClient([server])

        time_elapsed = 0
        timer = Timer(mem_client.get_stats)
        
        stats = mem_client.get_stats()
        #Messure the response time
        time_elapsed = timer.timeit(1)

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
        status_loc['response_time'] = round(self.stats_current[sid]['response_time'], 5)
        status_loc['bytes'] = round(int(self.stats_current[sid]['bytes'])/(1024*1024), 2)
        
        self.stats_new[sid] = status_loc

    def insert_records(self):
        '''Insert data to database'''

        for stats in self.stats_new:
            s_stat = self.stats_new[stats]
            MDatabase.insert_statistic(stats, s_stat)
