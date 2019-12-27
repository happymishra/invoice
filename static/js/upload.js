// https://www.mkyong.com/jquery/jquery-ajax-submit-a-multipart-form/

$(document).ready(function(){
    $('#upload').click(function(){
//        var file = $('#invoice-file')[0];
//        var data = new FormData()
//        data.append('file', file)

        var formData = new FormData();
        formData.append('file_path', $('#invoice-file')[0].files[0]);
//        var data = new FormData(file)

        $.ajax({
            type: "POST",
            enctype: 'multipart/form-data',
            url: "/path/",
            data: formData,
            contentType: false,
            processData: false,
            cache: false,
            success: function(data) {
                console.log("File uploaded successfully")
            },
            error: function() {
                console.log("File upload failed")
            }
        })

    })
})