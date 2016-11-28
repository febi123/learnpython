
$('#predict-form').on('submit', function(event){
    event.preventDefault();
    predictasync();
});

// AJAX for posting
function predictasync() {
    $('#predictionresult').text('');
    var nama = $("#nama").val()
    var suku = $("#suku").val()
    if(nama ==""){
        alert('Isikan nama telebih dahulu');
        return;
    }
    $('.btn').button('loading');
    //setTimeout(function () {
    //    $this.button('reset');
    //}, 8000);
    $.ajax({
        url: "predictasync/", // the endpoint
        type: "POST", // http method,
        csrfmiddlewaretoken: '{{ csrf_token }}',
        data: {'nama': nama, 'suku': suku }, // data sent with the post request // the_post: $('#post-text').val()

        // handle a successful response
        success: function (json) {

            var textres = ( json['jk']=='1' ? 'Laki-Laki' : 'Perempuan' ) + (' with probability ') + json['prob']
            $('#predictionresult').text(textres);

        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        },

        // completed
        complete: function (data) {
            $('.btn').button('reset');
        }
    });
};
