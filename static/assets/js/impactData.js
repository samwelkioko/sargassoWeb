const ctx = document.getElementById('plasticChart').getContext('2d');
let plasticChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: [], // Start with empty, will be filled by fetch
    datasets: [{
      label: 'Plastic Collected (kg)',
      data: [],
      backgroundColor: 'rgb(6, 214, 160)',
      borderColor: 'rgba((6, 214, 160, 1)',
      borderWidth: 1,
      borderRadius: 5
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Kg Collected' }
      }
    }
  }
});

// Initial fetch to populate chart
fetch('chart-data')
  .then(response => response.json())
  .then(data => {
    plasticChart.data.labels = data.labels;
    plasticChart.data.datasets[0].data = data.values;
    plasticChart.update();
  });

  // 🔁 JavaScript: Update chart when year changes
  document.getElementById('yearFilter').addEventListener('change', function () {
    const selectedYear = this.value;
    const url = `chart-data/?year=${selectedYear}`;

    fetch(url)
      .then(response => response.json())
      .then(data => {
        plasticChart.data.labels = data.labels;
        plasticChart.data.datasets[0].data = data.values;
        plasticChart.update();
      });
  });
  
    document.querySelectorAll('.counter').forEach(counter => {
      const target = +counter.getAttribute('data-target');
      let count = 0;
      const step = target / 60;

      const updateCount = () => {
        if (count < target) {
          count += step;
          counter.textContent = Math.ceil(count);
          requestAnimationFrame(updateCount);
        } else {
          counter.textContent = target;
        }
      };
      updateCount();
    });
