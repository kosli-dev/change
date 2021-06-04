'use strict';

$(document).ready(function () {
   // Open a non-local href target in a new tab/window whilst avoiding
   // a wrestling match with non-existent Sphinx nodes documentation.
   const $hrefs = $("a[href^='http']");
   $hrefs.attr('target','_blank');
   $hrefs.attr('rel', 'noopener noreferrer'); // secure linking site

   // This fix is used because of the legacy situation, a better solution
   // will have to be implemented
   const $topLevelLinks = $('.toctree-l1>a');
   $topLevelLinks.each(function() {
      const $link = $(this);
      if ($link.text().trim() === 'Quick Start'){
         $link.attr('href', '../tutorial/pipefile.html')
      }
      if ($link.text().trim() === 'Concepts'){
         $link.attr('href', '../concepts/devops_change_is_the_new_normal.html')
      }
      if ($link.text().trim() === 'Command Reference'){
         $link.attr('href', '../reference/declare_pipeline.html')
      }
      if ($link.text().trim() === 'Fingerprint Reference'){
         $link.attr('href', '../fingerprints/docker_fingerprint.html')
      }
   });
});