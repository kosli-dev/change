
$(document).ready(function () {
   // Open a non-local href target in a new tab/window whilst also
   // not wrestling with non-existent Sphinx nodes documentation.
   $("a[href^='http']").attr('target','_blank');
});