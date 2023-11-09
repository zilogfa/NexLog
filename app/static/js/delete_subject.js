$(document).ready(function() {
    $('.delete-subject').click(function(e) {
        e.preventDefault();
        var subjectId = $(this).data('subject-id'); // Corrected data attribute name
        var result = confirm("Are you sure you want to delete this subject?");
        
        if (result) {
            $.ajax({
                url: '/auth/delete_subject/' + subjectId, // Make sure the path is correct
                type: 'POST', // or 'DELETE' if you decide to change it
                data: {},
                headers: { "X-CSRF-Token": $('meta[name="csrf-token"]').attr('content') }, // Corrected header name
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
