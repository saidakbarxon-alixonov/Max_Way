// Dashboard behaviour. It replaces the 1,672-line theme demo file:
// only four things are needed on these pages.
(function ($) {
    "use strict";

    // 1. Page fade-in. animsition.css hides .animsition (opacity: 0) until this runs.
    $(".animsition").animsition({
        inClass: "fade-in",
        outClass: "fade-out",
        inDuration: 900,
        outDuration: 900,
        linkElement: 'a:not([target="_blank"]):not([href^="#"])',
        loading: true,
        loadingParentElement: "html",
        loadingClass: "page-loader",
        loadingInner: '<div class="page-loader__spin"></div>',
        timeout: false,
        onLoadEvent: true,
        browser: ["animation-duration", "-webkit-animation-duration"],
        overlay: false,
        transition: function (url) { window.location.href = url; }
    });

    // 2. Account dropdown in the top bar (the theme CSS shows it with .show-dropdown)
    var $account = $(".js-item-menu");
    $account.on("click", function (event) {
        event.preventDefault();
        $(this).toggleClass("show-dropdown");
    });
    // clicks inside the dropdown (Logout) must not reach the toggle above
    $(".js-dropdown").on("click", function (event) { event.stopPropagation(); });
    // a click anywhere else closes it
    $(document).on("click", function () { $account.removeClass("show-dropdown"); });

    // 3. Scrollbar of the sidebar
    if (document.querySelector(".js-scrollbar1")) {
        new PerfectScrollbar(".js-scrollbar1");
    }

    // 4. Tooltips on the edit / delete buttons
    $('[data-toggle="tooltip"]').tooltip();
})(jQuery);
