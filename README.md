#memdash
=======

A dashboard for clustered memcached servers

![Screenshot of memdash](https://github.com/gamunuud/memdash/raw/screenshot.png)

## Installation and Usage

MemDash requires following python libraries,

[CherryPy](http://www.cherrypy.org/) A Minimalist Python Web Framework
[pywin32](http://sourceforge.net/projects/pywin32/) if using as a windows service

CherryPy can be easily installed via common Python package managers such as setuptools or pip.

```
$ easy_install cherrypy
```
```
$ pip install cherrypy
```

You may also get the latest CherryPy version by grabbing the source code from BitBucket:

```
$ hg clone https://bitbucket.org/cherrypy/cherrypy
$ cd cherrypy
$ python setup.py install
```

###Usage

#####To run MemDash as a windows service

Open cmd/PowerShell and cd into directory and type

```
python mdservice.py install
```

start service

```
python mdservice.py start
```

stop service 

```
python mdservice.py stop
```

remove service
```
python mdservice.py remove
```

##### Direct start the server

```
$ python memdash.py
```

The web interface can be accessed by navigating to [http://172.0.0.1:8989](http://172.0.0.1:8989)

There are other ways to run this server on Linux, OSX sytems
to find out look into the [CherryPy documentation](http://docs.cherrypy.org/en/latest/)

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
