$(function() {
    $('#selectedBranch').change(function() {
        $.ajax({
        url: '/selected_branch/',
        data: {
          'branch': $('#selectedBranch').val()
        },
        dataType: 'json',
        success: function (data) {
            console.log("Commits");
        }
        });
    });
});