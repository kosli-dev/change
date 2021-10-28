'use strict';

$(document).ready(function () {
   // Open a non-local href target in a new tab/window whilst avoiding
   // a wrestling match with non-existent Sphinx nodes documentation.
   const $hrefs = $("a[href^='http']");
   $hrefs.attr('target','_blank');
   $hrefs.attr('rel', 'noopener noreferrer'); // secure linking site

   // This fix is used because of the legacy situation, a better solution
   // will have to be implemented
   const $topLevelLinks = $('.bd-sidebar .toctree-l1>a');
   $topLevelLinks.each(function(index) {
      const $link = $(this);
      let newLink;

      if ($link.text().trim() === 'Quick Start'){
         newLink = '../tutorial/pipefile.html';
      }
      if ($link.text().trim() === 'Concepts'){
         newLink = '../concepts/devops_change_is_the_new_normal.html';
      }
      if ($link.text().trim() === 'Command Reference'){
         newLink = '../reference/echo_fingerprint.html';
      }
      if ($link.text().trim() === 'Fingerprint Reference'){
         newLink = '../fingerprints/docker_fingerprint.html';
      }

      const checkbox = `<input class="toctree-checkbox" name="toctree-checkbox-${index + 2}" type="checkbox">
                        <label for="toctree-checkbox-${index + 2}">
                           <a href="${newLink}">
                              <i class="fas fa-chevron-down"></i>
                           </a>
                        </label>`

      $link.attr('href', newLink);
      $link.parent().not('.active').append(checkbox);


   });
});