if ( ! $.fn.dataTable.isDataTable( '#table-rights-user' ) ) {
    $('#table-rights-user').DataTable({
        "scrollY": "226px",
        "iDisplayLength": 5,
        "scrollCollapse": true,
        "lengthMenu": [5, 10, 15, 20],
        "columnDefs": [
            {"className": "dt-center", "targets": 0}
        ],
        order: [[0, 'asc']],
        "columns": [ null, { "orderable": false }, { "orderable": false }, { "orderable": false } ]
    });
}

if ( ! $.fn.dataTable.isDataTable( '#table-rights-group' ) ) {
    $('#table-rights-group').DataTable({
        "scrollY": "226px",
        "iDisplayLength": 5,
        "scrollCollapse": true,
        "lengthMenu": [5, 10, 15, 20],
        "columnDefs": [
            {"className": "dt-center", "targets": 0}
        ],
        order: [[0, 'asc']],
        "columns": [ null, { "orderable": false }, { "orderable": false }, { "orderable": false } ]
    });
}
