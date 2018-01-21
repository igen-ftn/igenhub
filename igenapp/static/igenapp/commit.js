$(function() {
    $('#selectedBranch').change(function() {
        var url = '/' + $('#owner_name').text() + '/' + $('#repo_name').text() + '/selected_branch/';
        $.ajax({
        url: url,
        data: {
          'branch': $('#selectedBranch').val()
        },
        dataType: 'json',
        success: function (data) {
            fillData(data);
        },
        error: function (data) {
            console.log(data);
        }
        });
    });

    function fillData(data) {
        $('#commitsContent').empty();

        for (var i in data.commits) {
            $('#commitsContent').append(
                "<div class=\"col-sm-8\">" +
                    "<div class=\"panel panel-white post panel-shadow\">" +
                        "<div class=\"post-heading1\">" +
                            "<div class=\"pull-left image\">" +
                                "<img src=\"http://bootdey.com/img/Content/user_1.jpg\" class=\"img-circle avatar1\" alt=\"user profile image\">" +
                            "</div>" +
                            "<div class=\"pull-left meta\">" +
                                "<div class=\"title mt\" style=\"white-space: nowrap;overflow: hidden;text-overflow: ellipsis;max-width: 520px;\" >" +
                                    "<a href=\"/" + data.owner_name + "/" + data.repo_name + "/commit/" + data.commits[i].sha + "/\">" + data.commits[i].commit.message + "</a>" +
                                "</div>" +
                                "<h6 class=\"text-muted time\">Committed by: <b>" + data.commits[i].commit.author.name + "</b></h6>" +
                            "</div>" +
                            "<div class=\"col-sm-2\" style=\"float:right; width: 55px;\">" +
                                "<a href=\"/" + data.owner_name + "/" + data.repo_name + "/commit/" + data.commits[i].sha + "/\" class=\"btn btn-success btn-circle text-uppercase\"><span class=\"glyphicon glyphicon-th-large\"></span></a>" +
                            "</div>" +
                        "</div>" +
                    "</div>" +
                "</div>"
            );
        }
    }
});