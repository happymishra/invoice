$(document).ready(function(){
    $('#upload').click(function(){
        var formData = new FormData();
        formData.append('file_path', $('#invoice-file')[0].files[0]);

        $.ajax({
            type: "POST",
            enctype: 'multipart/form-data',
            url: "api/invoice/upload/",
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