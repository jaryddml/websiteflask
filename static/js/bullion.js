// Function to handle sort preference change and sort current results
function sortResults() {
    const sortOrder = document.getElementById('sortPrice').value;
    localStorage.setItem('sortOrder', sortOrder); // Store sorting preference
    sortAndReorderResults();
}

// Function to sort and reorder results according to the stored sort order
function sortAndReorderResults() {
    const sortOrder = localStorage.getItem('sortOrder') || 'price_asc'; // Default to ascending
    const resultsContainer = document.querySelector('.results-container');
    let results = Array.from(resultsContainer.getElementsByClassName('result-item'));

    results.sort((a, b) => {
        let priceA = parseFloat(a.querySelector('.price').textContent.replace('$', '').replace(',', '').trim());
        let priceB = parseFloat(b.querySelector('.price').textContent.replace('$', '').replace(',', '').trim());
        return sortOrder === 'price_asc' ? priceA - priceB : priceB - priceA;
    });

    resultsContainer.innerHTML = ''; // Clear current results
    results.forEach(result => resultsContainer.appendChild(result)); // Re-append sorted results
}

// Function to dynamically load more results
let isLoading = false;
let nextPage = 2; // Assuming the first page is already loaded
window.onscroll = function() {
    // Check if the user has scrolled to near the bottom of the page
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100 && !isLoading) {
        isLoading = true;
        loadMoreResults();
    }
};

function loadMoreResults() {
    const sortOrder = localStorage.getItem('sortOrder') || 'price_asc'; // Default to ascending
    fetch(`/app/results?page=${nextPage}&sortOrder=${sortOrder}`, { // Adjust endpoint as necessary
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.results && data.results.length > 0) {
            const resultsContainer = document.querySelector('.results-container');
            data.results.forEach(result => {
                const item = document.createElement('li');
                item.className = 'result-item';
                // Build and append the result item to the container
                // This requires constructing the inner HTML of each result based on your template
                resultsContainer.appendChild(item);
            });
            nextPage++;
            isLoading = false;
            sortAndReorderResults(); // Re-sort the results including the newly added ones
        }
    })
    .catch(error => {
        console.error('Error loading more results:', error);
        isLoading = false;
    });
}

// Apply stored sort order on initial load
document.addEventListener('DOMContentLoaded', function() {
    if (localStorage.getItem('sortOrder')) {
        sortAndReorderResults();
    }
});
