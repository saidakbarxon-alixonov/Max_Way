// Bar chart "Products by category" on the main dashboard.
// The data comes from the template: {{ categories_products|json_script:"chart-data" }}
// NOTE: the options use the Chart.js 2 format (legend, xAxes, yAxes).
// If Chart.js is upgraded to 3 or 4 they become plugins.legend and scales.x / scales.y.
(function () {
    var canvas = document.getElementById("Chart1");
    var dataElement = document.getElementById("chart-data");
    if (!canvas || !dataElement || typeof Chart === "undefined") return;

    var rows = JSON.parse(dataElement.textContent);
    canvas.height = 150;

    new Chart(canvas, {
        type: "bar",
        data: {
            labels: rows.map(function (row) { return row.category; }),
            datasets: [{
                label: "Products",
                data: rows.map(function (row) { return row.product; }),
                borderColor: "rgba(0, 123, 255, 0.9)",
                borderWidth: 0,
                backgroundColor: "rgba(0, 123, 255, 0.5)"
            }]
        },
        options: {
            legend: { position: "top", labels: { fontFamily: "Poppins" } },
            scales: {
                xAxes: [{ ticks: { fontFamily: "Poppins" } }],
                yAxes: [{ ticks: { beginAtZero: true, fontFamily: "Poppins" } }]
            }
        }
    });
})();
