$(document).ready(function() {
    $('.delete-post').click(function(e) {
        e.preventDefault();
        var postId = $(this).data('post-id');
        var result = confirm("Are you sure you want to delete this subject?");
        
        if (result) {
            $.ajax({
                url: '/auth/delete_post/' + postId, // delete path
                type: 'POST', // or 'DELETE'
                data: {},
                headers: { "X-CSRF-Token": $('meta[name="csrf-token"]').attr('content') },
                success: function(response) {
                    if(response.status === 'success') {
                        window.location.reload();
                    } else {
                        alert('Error: ' + response.message);
                    }
                },
                error: function(error) {
                    console.log(error);
                    alert('An error occurred while deleting the subject.');
                }
            });
        }
    });
});
