document.getElementById('userForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = {
        age: document.getElementById('age').value,
        gpa: document.getElementById('gpa').value,
        financial_aid: document.getElementById('financial_aid').value
    };

    fetch('https://us-east1-outstanding-map-421217.cloudfunctions.net/insert_data', {
    method: 'POST',
    mode: 'no-cors', // Now correctly placed in the fetch options
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData),
})
.then(response => {
    console.log('Success:', response); // You cannot read the response details, but you can check if the fetch was not rejected
})
.catch((error) => {
    console.error('Error:', error);
});
});
