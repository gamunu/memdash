/*jslint browser: true*/
/*global $, jQuery, alert*/
window.alert = function (text) {
    'use strict';
    console.log('tried to alert: ' + text);
    return true;
};

var $genaral = $('#general-stats'), $statics_table, $slabs_table, $sizes_table,
$items_table, $settings_table, $title = $('.stats-title'),
$refreshtime = $('#refresh-time'), timer = 0;

var requests = {
    genaral : null,
    slabs : null,
    items : null,
    settings : null,
    url : 'localhost'
};

function writeLastRefresh() {
    'use strict';
    var minutes = Math.floor(timer / 60); // 7
    var seconds = timer % 60; // 30
    
    $refreshtime.text(minutes + ':' + seconds);
}

function fetchData(url) {
    'use strict';
    requests.url = url;
    
    if (requests.genaral !== null) {
        requests.genaral.abort();
        requests.slabs.abort();
        requests.items.abort();
        requests.settings.abort();
    }
    
    $.get('stats', { server : url }, function (data) {
            $genaral.html(data);
        });
    
    requests.genaral = $.get('statst', { server : url },
                                function (data) {
                                    if (data.length > 0) {
                                        $statics_table.fnAddData(data);
                                    }
                                });
        
    requests.slabs = $.get('slabs', { server : url },
                                function (data) {
                                    if (data.length > 0) {
                                        $slabs_table.fnAddData(data);
                                    }
                                });
        
    requests.items = $.get('items', { server : url },
                                function (data) {
                                    if (data.length > 0) {
                                        $items_table.fnAddData(data);
                                    }
                                });
        
    requests.settings = $.get('settings', { server : url },
                                function (data) {
                                    if (data.length > 0) {
                                        $settings_table.fnAddData(data);
                                    }
                                });
}

function initDataTables() {
    'use strict';
    //connect to the server before getting informaton
    //stats tab
    //Get generatl stats
    $.get('first')
    .done(function (data) {
        var url = data.server;
        $statics_table = $('#statics-table').dataTable();
        $slabs_table = $('#slabs-table').dataTable();
        $items_table = $('#items-table').dataTable();
        $settings_table = $('#settings-table').dataTable();
        $sizes_table = $('#sizes-table').dataTable();
        $title.text(url);
        fetchData(url);
    });
}

function clearTables() {
    'use strict';
    $statics_table.api().clear().draw();
    $slabs_table.api().clear().draw();
    //$sizes_table.api().ajax.reload();
    $items_table.api().clear().draw();
    $settings_table.api().clear().draw();
}

function changeServer(url) {
    'use strict';
    $title.text(url);
    $genaral.html('');
    //clear tables
    clearTables();
    fetchData(url);
}

$(document).ready(function () {
    'use strict';
    
    $.get('servers', function (data) {
        var $list = $('#list');
        $list.html(data);
    })
    .done(function () {
        //connect to the server before getting informaton
        initDataTables();
    });
    
    $(document).on('click', '#list li', function (e) {
        $('#list li.active').removeClass('active');
        var $this = $(this);
        if (!$this.hasClass('active')) {
            $this.addClass('active');
        }
        
        var server = $this.data('server');
        changeServer(server);
        e.preventDefault();
    });
    
    $(document).on('click', '#getitemstats', function (e) {
        $sizes_table.api().clear().draw();
        $.get('sizes', { server : requests.url },
                                function (data) {
                                    if (data.length > 0) {
                                        $sizes_table.fnAddData(data);
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
        
        clearTables();
        changeServer(requests.url);
        timer = 0;
    }, 300000);
    
    //count up timer
    setInterval(function () {
        timer += 1;
        var minutes = Math.floor(timer / 60); // 7
        var seconds = timer % 60; // 30
        
        $refreshtime.text(minutes + 'min and ' + seconds + 's ago');
    }, 1000);
});