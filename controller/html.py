#!/usr/bin/env python3
'''Methods for getting parts of web pages'''

from datetime import date
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('views'))

class Html(object):
    '''Methods for getting parts of web pages'''

    @staticmethod
    def get_navigation(page='home'):
        '''Creates html navigation for pages
        according to the argument page
        @return: html string
        @rtype: str'''
        nav = []
        nav.append('''<nav class="navbar navbar-inverse navbar-fixed-top"
                   role="navigation">
           <div class="container-fluid">
             <!-- Brand and toggle get grouped for better mobile display -->
             <div class="navbar-header">
               <button type="button" class="navbar-toggle collapsed"  data-toggle="collapse" data-target="#mnavbar" aria-expanded="false" >
                 <span class="sr-only">Toggle navigation</span>
                 <span class="icon-bar"></span>
                 <span class="icon-bar"></span>
                 <span class="icon-bar"></span>
               </button>
               <a class="navbar-brand" href="/">MemDash</a>
             </div>

             <!-- Collect the nav links, forms, and other content for toggling -->
             <div class="collapse navbar-collapse" id="mnavbar">
               <ul class="nav navbar-nav">
               ''')
        navitems = []
        navitems.append({
            'title' : 'Detail View',
            'url' : '/detail',
            'id' : 'detail'
            })

        for item in navitems:
            if item['id'] == page:
                nav.append('<li class="{}">'
                           '<a href="{}" >{}</a>'
                           '</li>'.format('active', item['url'], item['title']))
            else:
                nav.append('<li class="{}">'
                           '<a href="{}" >{}</a>'
                           '</li>'.format('', item['url'], item['title']))
        nav.append('''</ul><ul class="nav navbar-nav navbar-right">
                 <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Stats Help<span class="caret"></span></a>
                  <ul class="dropdown-menu" role="menu">
                    <li><a href="#" data-toggle="modal" data-target="#general-help">General-purpose statistics</a></li>
                    <li><a href="#" data-toggle="modal" data-target="#settings-help">Settings statistics</a></li>
                    <li><a href="#" data-toggle="modal" data-target="#settings-help">Something else here</a></li>
                    <li><a href="#" data-toggle="modal" data-target="#item-help">Item statistics</a></li>
                    <li><a href="#" data-toggle="modal" data-target="#itemsize-help">Item size statistics</a></li>
                    <li><a href="#" data-toggle="modal" data-target="#slabs-help">Slab statistics</a></li>
                  </ul>
                </li>
                <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Manage<span class="caret"></span></a>
                  <ul class="dropdown-menu" role="menu">
                    <li><a href="/admin">Add/Remove Servers</a></li>
                  </ul>
                </li>
              </ul>''')
        nav.append('''</div><!-- /.navbar-collapse -->
                        </div><!-- /.container-fluid -->
                    </nav>''')

        return ''.join(nav)
