
function editComment(comment, comment_id) {
    editForm = '<textarea name="content" class="form-control">' + comment + '</textarea>' + '<input type="hidden" name="comment_id" value="' + comment_id + '">' + '<input type="submit" class="btn btn-success pull-right" value="Save">';
    element_id = 'editCom' + comment_id
    document.getElementById(element_id).innerHTML = editForm;
}
