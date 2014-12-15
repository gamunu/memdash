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
Chart.defaults.Line.scaleFontColor = "#222";
Chart.defaults.Line.responsive = true;
Chart.defaults.Line.pointDotRadius = 2;

var Memdash = {
    genaral: $('.general-stats'),
    statics_table: null,
    gen_connections: $('#gen-connections'),
    gen_items: $('#gen-items'),
    gen_cashits: $('#gen-cashits'),
    gen_casmisses: $('#gen-casmisses'),
    gen_getcom: $('#gen-getcom'),
    gen_setcom: $('#gen-setcom'),
    storage_message: $('#storage-message'),
    storage_progress: $('#storage-progress'),
    command_message: $('#command-message'),
    command_progress: $('#command-progress'),
    refresh_time: $('#refresh-time'),
    timer: 0,
    
    //graphs dom
    $graph_hits: $("#hits-misses"),
    $graph_cmds: $("#graph-cmds"),
    $graph_cache: $("#graph-cacheditems"),
    $graph_memory: $("#graph-memory"),
    
    changeGraphToDate: function (start, end) {
        'use strict';
        var self = this;
        this.graphmemory.destroy();
        this.cacheditems.destroy();
        this.gcmds.destroy();
        this.ghits.destroy();
        
        $.get('graph/ovhits',
              {
                startdate : start,
                enddate : end
            },
            function (data) {
                var ctx = self.$graph_hits.get(0).getContext("2d");
                self.ghits = new Chart(ctx).Line(data);
                if (data.labels.length > 0) {
                    self.$graph_hits.hide().fadeIn('slow');
                }
                else {
                    self.$graph_hits.hide();
                }
            });
        
        $.get('graph/ovcmds',
              {
                startdate : start,
                enddate : end
            },
            function (data) {
                var ctx = self.$graph_cmds.get(0).getContext("2d");
                self.gcmds = new Chart(ctx).Line(data);
                if (data.labels.length > 0) {
                    self.$graph_cmds.hide().fadeIn('slow');
                }
                else {
                    self.$graph_cmds.hide();
                }
            });
        
        $.get('graph/ovcacheditems',
              {
                startdate : start,
                enddate : end
            },
            function (data) {
                var ctx = self.$graph_cache.get(0).getContext("2d");
                self.cacheditems = new Chart(ctx).Line(data);
                if (data.labels.length > 0) {
                    self.$graph_cache.hide().fadeIn('slow');
                }
                else {
                    self.$graph_cache.hide();
                }
            });
        
        $.get('graph/ovmemory',
              {
                startdate : start,
                enddate : end
            },
            function (data) {
                var ctx = self.$graph_memory.get(0).getContext("2d");
                self.graphmemory = new Chart(ctx).Line(data);
                if (data.labels.length > 0) {
                    self.$graph_memory.hide().fadeIn('slow');
                }
                else {
                    self.$graph_memory.hide();
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
            $.get('onlinservers', function (data) {
                $('.server-onoff').html(data);
            });
    
            $.get('service', function (data) {
                //fill stats table
                self.statics_table = $('#global-statics-table').dataTable({
                    'data' : data.data
                });
                self.genaral.html(data.overall);
            });
        });
        
        $.get('graph/ovhits', function (data) {
            var ctx = self.$graph_hits.get(0).getContext("2d");
            self.ghits = new Chart(ctx).Line(data);
            if (data.labels.length > 0) {
                self.$graph_hits.hide().fadeIn('slow');
            }
            else {
                self.$graph_hits.hide();
            }
        });
        
        $.get('graph/ovcmds', function (data) {
            var ctx = self.$graph_cmds.get(0).getContext("2d");
            self.gcmds = new Chart(ctx).Line(data);
            if (data.labels.length > 0) {
                self.$graph_cmds.hide().fadeIn('slow');
            }
            else {
                self.$graph_cmds.hide();
            }
        });
        
        $.get('graph/ovcacheditems', function (data) {
            var ctx = self.$graph_cache.get(0).getContext("2d");
            self.cacheditems = new Chart(ctx).Line(data);
            if (data.labels.length > 0) {
                self.$graph_cache.hide().fadeIn('slow');
            }
            else {
                self.$graph_cache.hide();
            }
        });
        
        $.get('graph/ovmemory', function (data) {
            var ctx = self.$graph_memory.get(0).getContext("2d");
            self.graphmemory = new Chart(ctx).Line(data);
            if (data.labels.length > 0) {
                self.$graph_memory.hide().fadeIn('slow');
            }
            else {
                self.$graph_memory.hide();
            }
        });
    }
};

$(document).ready(function () {
    'use strict';

    $.get('servers', function (data) {
        var $list = $('#list');
        $list.html(data);
    })
    .done(function () {
        //connect to the server before getting informaton
        Memdash.initDataTables();
    });

    $('body').tooltip({
        selector: '[rel=tooltip]'
    });

    setInterval(function () {
        Memdash.statics_table.api().clear().draw();

        $.get('onlinservers', function (data) {
            $('.server-onoff').html(data);
        });

        $.get('service', function (data) {
            //fill stats table
            if (data.data.length > 0) {
                Memdash.statics_table.fnAddData(data.data);
                Memdash.genaral.html(data.overall);
            }
        });
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