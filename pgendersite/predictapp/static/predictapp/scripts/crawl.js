
$('#runmodel-form').on('submit', function(event){
    event.preventDefault();
    runmodel();
});

// AJAX for posting
function runmodel() {
    console.log("create post is working!") // sanity check
    $('.btn').button('loading');
    //setTimeout(function () {
    //    $this.button('reset');
    //}, 8000);

    $.ajax({
        url: "runmodel/", // the endpoint
        type: "POST", // http method
        data: {}, // data sent with the post request // the_post: $('#post-text').val()

        // handle a successful response
        success: function (json) {
            //$('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
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
