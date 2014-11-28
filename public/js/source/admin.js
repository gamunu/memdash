/*jslint browser: true*/
/*global $, jQuery, bootbox, alert*/
function alertSuccess(msg)
{
    'use strict';
    var html = [
            '<div class="alert alert-success" role="alert">',
            '<button type="button" class="close" data-dismiss="alert">',
            '<span aria-hidden="true">&times;</span>',
            '<span class="sr-only">Close</span>',
            '</button>',
            msg,
            '</div>'
        ].join('');
    return html;
}

function alertError(msg)
{
    'use strict';
    var html = [
            '<div class="alert alert-danger" role="alert">',
            '<button type="button" class="close" data-dismiss="alert">',
            '<span aria-hidden="true">&times;</span>',
            '<span class="sr-only">Close</span>',
            '</button>',
            msg,
            '</div>'
        ].join('');
    return html;
}

$(document).ready(function () {
    'use strict';
    var $list = $('#servers tbody'), $servername = $('#server-name'),
    $serverport = $('#server-port'), $eservername = $('#eserver-name'),
    $eserverport = $('#eserver-port'), updateid, $message = $('#message'),
    $u_server = null, $u_port = null;
    
    $.get('servers', function (data) {
        $list.append(data);
    });
    
    $(document).on('click', '#insert-server', function (event) {
        var sname = $servername.val(),
        port = $serverport.val();
        $.post(
               'insert',
               { name: sname, port: port},
                function (data) {
                    if (data.id > 0) {
                        var html = [
                            '<tr><td>',
                            sname,
                            '</td><td>',
                            port,
                            '</td></td><td>',
                            '<button type="button" class="btn btn-danger delete-server" data-id="',
                            data.id,
                            '">Delete</button></td>',
                            '<td><button type="button" class="btn btn-primary update-server" data-id="',
                            data.id,
                            '">Update</button></td>'
                        ].join('');
                        $list.append(html);
                        $message.html(alertSuccess('Successfully added : ' + sname));
                    }
                    else {
                        $message.html(alertError(sname + 'Adding failed'));
                    }
                    $('#additem').modal('hide');
                });
    });
    
    $(document).on('click', '.delete-server', function (event) {
        var $this = $(this);
        bootbox.confirm("Are you sure?", function (result) {
            if (result) {
                var id = $this.data('id');
                $.get('delete', { sid : id }, function (data) {
                    
                    if (data.msg) {
                        $this.closest("tr")
                        .fadeOut(500, function () { $(this).remove(); });
                        $message.html(alertSuccess('Successfully deleted'));
                    }
                    else {
                        $message.html(alertSuccess('Delete falied'));
                    }
                    
                    
                });
            }
        });
    });
    
    $(document).on('click', '.update-server', function (event) {
        var $this = $(this), $parent = $this.closest("tr");
        $u_server = $parent.find('td.data-server');
        $u_port = $parent.find('td.data-port');
        updateid = $this.data('id');
        
        $eservername.val($u_server.text());
        $eserverport.val($u_port.text());
        
        $('#updateitem').modal('show');
    });
    
    $(document).on('click', '#update-server', function (event) {
        var name = $eservername.val(),
        port = $eserverport.val();
        
        $.post('update',
                {
                name: name,
                port: port,
                sid : updateid
            },
                function (data) {
                    if (data.msg) {
                        $u_server.text(name);
                        $u_port.text(port);
                        $message.html(alertSuccess('Successfully updated : ' + name));
                    }
                    else {
                        $message.html(alertError(name + 'Update failed'));
                    }
                    $('#updateitem').modal('hide');
                });
    });
});