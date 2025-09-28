document.addEventListener('DOMContentLoaded', function () {
    const searchButton = document.querySelector('.search-button');
    const searchInput = document.querySelector('.search-bar');
    const resultsContainer = document.querySelector('.results-container');

    searchButton.addEventListener('click', function () {
        const query = searchInput.value.trim();
        if (!query) {
            resultsContainer.innerHTML = '<p>Please enter a search term.</p>';
            return;
        }

        fetch(`/api/tasks/search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = '';
                if (data.length === 0) {
                    resultsContainer.innerHTML = '<p>No results found.</p>';
                } else {
                    data.forEach(item => {
                        console.log("works")
                        const resultDiv = document.createElement('div');
                        resultDiv.classList.add('result-item');

                        // Title
                        const title = document.createElement('h3');
                        title.classList.add('result-title');
                        title.textContent = item.name;
                        resultDiv.appendChild(title);

                        // Description
                        const desc = document.createElement('p');
                        desc.classList.add('result-snippet');
                        desc.textContent = item.description;
                        resultDiv.appendChild(desc);

                        // Tasks (if exists)
                        if (item.task) {
                            const img = document.createElement('img');
                            img.classList.add('result-task');
                            img.src = item.task;
                            img.alt = item.name;
                            resultDiv.appendChild(img);

                            // Download link
                            const downloadPara = document.createElement('p');
                            const downloadLink = document.createElement('a');
                            downloadLink.classList.add('download-button');
                            downloadLink.href = item.task;
                            downloadLink.download = '';
                            downloadLink.textContent = 'Download';
                            downloadPara.appendChild(downloadLink);
                            resultDiv.appendChild(downloadPara);
                        }

                        resultsContainer.appendChild(resultDiv);
                    });
                }
            })
            .catch(error => {
                resultsContainer.innerHTML = '<p>Error fetching results.</p>';
                console.error('Fetch error:', error);
            });
    });
});
