document.addEventListener("DOMContentLoaded", function() {
    $('#jstree').jstree({
        'core': {
            'data': {
                'url': '/tree_data/',
                'dataType': 'json'
            }
        }
    });
});
