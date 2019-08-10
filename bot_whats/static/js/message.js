$(document).ready(function () {
  (function($) {
    "use strict";

    // Configure tooltips for collapsed side navigation
    $('.navbar-sidenav [data-toggle="tooltip"]').tooltip({
      template: '<div class="tooltip navbar-sidenav-tooltip" role="tooltip" style="pointer-events: none;"><div class="arrow"></div><div class="tooltip-inner"></div></div>'
    })

    // Configure tooltips globally
    $('[data-toggle="tooltip"]').tooltip()
  })(jQuery);


});