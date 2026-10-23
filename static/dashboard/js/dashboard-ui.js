// Small behaviours shared by the dashboard pages. Plain JavaScript, no jQuery.
(function () {
    // 1. Ask before submitting a form that has data-confirm (the delete buttons).
    document.addEventListener("submit", function (event) {
        var message = event.target.getAttribute("data-confirm");
        if (message && !window.confirm(message)) {
            event.preventDefault();
        }
    });

    // 2. Image preview: <input type="file" data-preview="#image-preview">
    document.addEventListener("change", function (event) {
        var input = event.target;
        var selector = input.getAttribute("data-preview");
        if (!selector || !input.files || !input.files[0]) return;

        var preview = document.querySelector(selector);
        if (!preview) return;

        var reader = new FileReader();
        reader.onload = function () {
            preview.src = reader.result;
            preview.hidden = false;
        };
        reader.readAsDataURL(input.files[0]);
    });
})();
