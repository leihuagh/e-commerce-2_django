$(document).ready(function() {
  function renderChart(id, data, labels) {
    // const ctx = document.getElementById("myChart").getContext('2d');
    const ctx = $("#" + id);
    let myChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Sales",
            data: data,
            backgroundColor: "rgba(0, 158, 29, 0.45)",
            borderColor: "rgba(0, 158, 29, 1)"
          }
        ]
      },
      options: {
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              }
            }
          ]
        },
        backgroundColor: "rgba(75, 192, 192, 1)"
      }
    });
  }
  function getSalesData(id, type) {
    const url = "/analytics/sales/data/";
    const method = "GET";
    let data = { type: type };
    $.ajax({
      url: url,
      method: method,
      data: data,
      success: function(responseData) {
        renderChart(id, responseData.data, responseData.labels);
      },
      error: function(error) {
        $.alert("An error occurred in charts");
        console.log("An error occurred while ajax call in chart js" + error);
      }
    });
  }
  const chartsToRender = $(".render-chart");
  $.each(chartsToRender, function(index, html) {
    const $this = $(this);
    if ($this.attr("id") && $this.attr("data-type")) {
      getSalesData($this.attr("id"), $this.attr("data-type"));
    }
  });
});