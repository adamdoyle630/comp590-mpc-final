document.getElementById('userForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = {
        age: document.getElementById('age').value,
        gpa: document.getElementById('gpa').value,
        financial_aid: document.getElementById('financial_aid').value
    };
    
    fetch('https://us-central1-outstanding-map-421217.cloudfunctions.net/insert_data', {
        method: 'POST',
        mode: 'no-cors', // Added to bypass CORS issues for development
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => {
        console.log('Success:', response); // Note: response will be opaque due to no-cors
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
