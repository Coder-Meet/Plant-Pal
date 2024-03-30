const form = document.getElementById('project-form');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  fetch('/submit-data', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json()) // Expect JSON response from server
  .then(data => {
    if (data.error) {
      alert('Error: ' + data.error);
      return;
    }
    // Update the DOM with analysis results (replace with actual display logic)
    document.getElementById('analysis-location').textContent = data.location;
    document.getElementById('analysis-budget').textContent = data.budget;
    document.getElementById('analysis-timeframe').textContent = data.timeframe;
    document.getElementById('analysis-has-image').textContent = data.has_image;
    if (data.analysis) {
      document.getElementById('analysis-results').textContent = data.analysis;
    } else {
      document.getElementById('analysis-results').textContent = 'No analysis available.';
    }
  })
  .catch(error => {
    console.error(error);
    alert('Error submitting data!');
  });
});
