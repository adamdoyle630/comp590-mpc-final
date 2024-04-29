document.getElementById('userForm').addEventListener('submit', function(e) {
    e.preventDefault();
  
    const formData = {
      age: parseInt(document.getElementById('age').value),
      gpa: parseFloat(document.getElementById('gpa').value),
      financial_aid: parseInt(document.getElementById('financial_aid').value)
    };

    console.log(JSON.stringify(formData))
  
    fetch('https://us-east1-outstanding-map-421217.cloudfunctions.net/insert_data', {
      method: 'POST',
      mode: 'no-cors', // Added to bypass CORS issues for development
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(formData),
    })
    .then(response => {
      // Check the response status
      if (response.ok) {
        // Display success message
        alert('Form submitted successfully!', 'success');
      } else {
        // Display error message
        alert('Failed to submit the form. Please try again.', 'error');
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      // Display error message
      alert('An error occurred while submitting the form.', 'error');
    });
  });
  