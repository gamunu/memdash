/*jslint browser: true*/
/*global $, jQuery, alert, Chart, moment*/
window.alert = function (text) {
    'use strict';
    console.log('tried to alert: ' + text);
    return true;
};

Chart.defaults.Line.scaleFontFamily = "'Raleway'";
Chart.defaults.Line.scaleFontStyle = "500";
Chart.defaults.Line.scaleFontSize = 14;
Chart.defaults.Line.scaleFontColor = "#555";
Chart.defaults.Line.responsive = true;
Chart.defaults.Line.pointDotRadius = 2;

var Memdash = {
    general: $('.general-stats'),
    statics_table: $('#statics-table').dataTable(),
    slabs_table: $('#slabs-table').dataTable(),
    sizes_table: $('#sizes-table').dataTable(),
    items_table: $('#items-table').dataTable(),
    settings_table: $('#settings-table').dataTable(),
    title: $('.stats-title'),
    refresh_time: $('#refresh-time'),
    timer: 0,
    
    //graphs dom
    $graph_hits: $("#hits-misses"),
    $graph_cmds: $("#graph-cmds"),
    $graph_cache: $("#graph-cacheditems"),
    $graph_memory: $("#graph-memory"),
    $graph_response: $("#graph-response"),
    
    requests: {
        general : null,
        slabs : null,
        items : null,
        settings : null,
        id : 'localhost'
    },
    
    writeLastRefresh: function () {
        'use strict';
        var minutes = Math.floor(this.timer / 60);
        var seconds = this.timer % 60;
        this.refresh_time.text(minutes + ':' + seconds);
    },

    changeGraphToDate: function (start, end) {
        'use strict';
        var self = this;
        this.graphmemory.destroy();
        this.cacheditems.destroy();
        this.graphresponse.destroy();
        this.gcmds.destroy();
        this.ghits.destroy();

        $.get('graph/hits',
              {
                server : this.requests.id,
                startdate : start,
                enddate : end
            },
            function (data) {
                var ctx = self.$graph_hits.get(0).getContext("2d");
                self.ghits = new Chart(ctx).Line(data);
            });
        
        $.get('graph/cmds',
              {
                server : this.requests.id,
                startdate : start,
                enddate : end
            },
            function (data) {
                var ctx = self.$graph_cmds.get(0).getContext("2d");
                Memdash.gcmds = new Chart(ctx).Line(data);
            });
        
        $.get('graph/cacheditems',
              {
                server : this.requests.id,
                startdate : start,
                enddate : end
            },
            function (data) {
                var ctx = self.$graph_cache.get(0).getContext("2d");
                self.cacheditems = new Chart(ctx).Line(data);
            });

        $.get('graph/memory',
              {
                server : this.requests.id,
                startdate : start,
                enddate : end
            },
            function (data) {
                var ctx = self.$graph_memory.get(0).getContext("2d");
                self.graphmemory = new Chart(ctx).Line(data);
            });

        $.get('graph/responsetime',
              {
                server : this.requests.id,
                startdate : start,
                enddate : end
            },
            function (data) {
                var ctx = self.$graph_response.get(0).getContext("2d");
                self.graphresponse = new Chart(ctx).Line(data);
            });
    },

    fetchData: function (id) {
        'use strict';
        this.requests.id = id;
        var self = this;
        
        if (this.requests.general !== null) {
            this.requests.general.abort();
            this.requests.slabs.abort();
            this.requests.items.abort();
            this.requests.settings.abort();
        }

        $.get('stats', { server : id }, function (data) {
                self.general.html(data.html).hide().fadeIn('slow');
                if (!data.online) {
                    $('.chart-row').fadeOut('slow');
                } else {
                    $('.chart-row').fadeIn('slow');
                }
            });

        $.get('graph/hits', { server : id }, function (data) {
            var ctx = self.$graph_hits.get(0).getContext("2d");
            self.ghits = new Chart(ctx).Line(data);
        });

        $.get('graph/cmds', { server : id }, function (data) {
            var ctx = self.$graph_cmds.get(0).getContext("2d");
            self.gcmds = new Chart(ctx).Line(data);
        });

        $.get('graph/cacheditems', { server : id }, function (data) {
            var ctx = self.$graph_cache.get(0).getContext("2d");
            self.cacheditems = new Chart(ctx).Line(data);
        });
        $.get('graph/memory', { server : id }, function (data) {
            var ctx = self.$graph_memory.get(0).getContext("2d");
            self.graphmemory = new Chart(ctx).Line(data);
        });

        $.get('graph/responsetime', { server : id }, function (data) {
            var ctx = self.$graph_response.get(0).getContext("2d");
            self.graphresponse = new Chart(ctx).Line(data);
        });

        this.requests.general = $.get('statst', { server : id },
                                    function (data) {
                                        if (data.length > 0) {
                                            self.statics_table.fnAddData(data);
                                        }
                                    });

        this.requests.slabs = $.get('slabs', { server : id },
                                    function (data) {
                                        if (data.length > 0) {
                                            self.slabs_table.fnAddData(data);
                                        }
                                    });

        this.requests.items = $.get('items', { server : id },
                                    function (data) {
                                        if (data.length > 0) {
                                            self.items_table.fnAddData(data);
                                        }
                                    });

        this.requests.settings = $.get('settings', { server : id },
                                    function (data) {
                                        if (data.length > 0) {
                                            self.settings_table.fnAddData(data);
                                        }
                                    });
    },
    
    initDataTables: function () {
        'use strict';
        var self = this;
        //connect to the server before getting informaton
        //stats tab
        //Get generatl stats
        $.get('first')
        .done(function (data) {
            var id = data.id;
            self.title.html(data.address);
            self.fetchData(id);
        });
    },
    clearTables: function () {
        'use strict';
        this.statics_table.api().clear().draw();
        this.slabs_table.api().clear().draw();
        this.items_table.api().clear().draw();
        this.settings_table.api().clear().draw();
        this.graphmemory.destroy();
        this.cacheditems.destroy();
        this.gcmds.destroy();
        this.ghits.destroy();
        this.graphresponse.destroy();
    },
    changeServer: function (id, server) {
        'use strict';
        this.title.html(server);
        //clear tables
        this.clearTables();
        this.fetchData(id);
    }
};

$(document).ready(function () {
    'use strict';
    
    $.get('servers', function (data) {
        var $list = $('#list');
        $list.html(data);
        Memdash.initDataTables();
    });

    $(document).on('click', '#list li', function (e) {
        $('#list li.active').removeClass('active');
        var $this = $(this);
        if (!$this.hasClass('active')) {
            $this.addClass('active');
        }

        var id = $this.data('id');
        var server = $this.data('server');
        Memdash.changeServer(id, server);
        e.preventDefault();
    });

    $(document).on('click', '#getitemstats', function (e) {
        Memdash.sizes_table.api().clear().draw();
        $.get('sizes', { server : Memdash.requests.id },
                                function (data) {
                                    if (data.length > 0) {
                                        Memdash.sizes_table.fnAddData(data);
                                    }
                                });
    });

    $('body').tooltip({
        selector: '[rel=tooltip]'
    });

    setInterval(function () {
        $.get('servers', function (data) {
            var $list = $('#list');
            $list.html(data);
        });

        Memdash.clearTables();
        Memdash.changeServer(Memdash.requests.id);
        Memdash.timer = 0;
    }, 300000);

    //count up timer
    setInterval(function () {
        Memdash.timer += 1;
        var minutes = Math.floor(Memdash.timer / 60); // 7
        var seconds = Memdash.timer % 60; // 30

        Memdash.refresh_time.text(minutes + 'min and ' + seconds + 's ago');
    }, 1000);


    var cb = function (start, end, label) {
        $('#reportrange span').html(start.format('MMMM D, YYYY HH:mm') + ' - ' + end.format('MMMM D, YYYY HH:mm'));
    };

    var optionSet1 = {
        startDate: moment().subtract(29, 'days'),
        endDate: moment(),
        minDate: '01/01/2012',
        maxDate: moment(),
        dateLimit: { days: 60 },
        showDropdowns: true,
        showWeekNumbers: true,
        timePicker: true,
        timePickerIncrement: 1,
        timePicker12Hour: true,
        ranges: {
            'Last 15 min. (resolution : 1 min. autorefresh)' : [moment().subtract(15, 'minutes'), moment()],
            'Last 1 Hour (resolution : 1 min.)' : [moment().subtract(1, 'hours'), moment()],
            'Last 2 Hours (resolution : 1 min.)' : [moment().subtract(2, 'hours'), moment()],
            'Last 3 Hours (resolution : 1 min.)' : [moment().subtract(3, 'hours'), moment()],
            'Last 4 Hours (resolution : 1 min.)' : [moment().subtract(4, 'hours'), moment()],
            'Last 6 Hours (resolution : 10 min..)' : [moment().subtract(6, 'hours'), moment()],
            'Last 12 Hours (resolution : 10 min.)' : [moment().subtract(12, 'hours'), moment()],
            'Last 24 Hours (resolution : 10 min.)': [moment().subtract(1, 'days'), moment()],
            'Today (resolution : 10 min.)': [moment().startOf('day'), moment().endOf('day')],
            'Last 1 Week (resolution : 1 hour.)': [moment().subtract(1, 'week'), moment()],
            'Last 2 Weeks (resolution : 1 hour.)': [moment().subtract(2, 'week'), moment()],
            'Last 1 Month (resolution : 1 hour.)': [moment().subtract(1, 'month'), moment()],
            'Last 3 Month (resolution : 1 hour.)': [moment().subtract(3, 'month'), moment()],
            'Last 6 Month (resolution : 1 hour.)': [moment().subtract(6, 'month'), moment()],
            'Last 1 Year (resolution : 1 hour.)': [moment().subtract(1, 'year'), moment()]
        },
        opens: 'left',
        buttonClasses: ['btn btn-default'],
        applyClass: 'btn-small btn-primary',
        cancelClass: 'btn-small',
        format: 'MM/DD/YYYY HH:mm',
        separator: ' to ',
        locale: {
            applyLabel: 'Apply',
            cancelLabel: 'Cancel',
            fromLabel: 'From',
            toLabel: 'To',
            customRangeLabel: 'Custom',
            daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr','Sa'],
            monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            firstDay: 1
        }
    };

    //Date range picker
    $('#reportrange span').html(moment().subtract(15, 'minutes').format('MMMM D, YYYY HH:mm') +
                                ' - ' + moment().format('MMMM D, YYYY HH:mm'));

    $('#reportrange').daterangepicker(optionSet1, cb);
    $('#reportrange').on('apply.daterangepicker', function (ev, picker) {
        Memdash.changeGraphToDate(picker.startDate.unix(), picker.endDate.unix());
    });
});