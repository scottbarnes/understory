/* for quotations */
window.onload = function() {
  setTimeout( function() {
    /* document.querySelector( '.quote' ).className = ( 'quote active' ); */
    var quotes = document.querySelectorAll( '.quote');
    [].forEach.call(quotes, function(quote) {
      quote.className = ( 'quote active');
    })
  }, 100 )
}
