$(document).ready(function() {
    $('#submit').submit(function() {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: '/ajax/save_data/',
            success: function(response) {
                console.log(response)
            }
        });
        return false;
    });
});