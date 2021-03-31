
$(document).ready(function () {
   // Open a non-local href target in a new tab/window whilst avoiding
   // a wrestling match with non-existent Sphinx nodes documentation.
   const hrefs = $("a[href^='http']");
   hrefs.attr('target','_blank');
   hrefs.attr('rel', 'noopener noreferrer'); // secure linking site
});
