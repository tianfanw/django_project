$(document).ready(function() {
  $('#ticket-table').dataTable();

  $('#price-button').click(function(e){
    e.preventDefault();
    $('#estimated-price').html('Calculating...');
    $.ajax({
      type: "GET",
      url: "/price",
      data: $('#price-form').serialize(),
      success: function(result) {
        $('#estimated-price').html(result['price']);
      },
      error: function (xhr, ajaxOptions, thrownError) {
        console.log(xhr.status);
        console.log(thrownError);
      }
    });
  });
});