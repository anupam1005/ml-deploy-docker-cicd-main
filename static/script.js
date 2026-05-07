document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = document.getElementById('predict-btn');
    const btnText = btn.querySelector('span');
    const resultArea = document.getElementById('result-area');
    const predictionText = document.getElementById('prediction-text');

    // Get input values
    const data = [
        parseFloat(document.getElementById('sepal_length').value),
        parseFloat(document.getElementById('sepal_width').value),
        parseFloat(document.getElementById('petal_length').value),
        parseFloat(document.getElementById('petal_width').value)
    ];

    // Loading state
    btn.disabled = true;
    btnText.textContent = 'Analyzing...';
    resultArea.classList.add('hidden');

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data: data })
        });

        if (!response.ok) {
            throw new Error('Prediction failed');
        }

        const result = await response.json();
        const speciesMap = ['Iris-Setosa', 'Iris-Versicolour', 'Iris-Virginica'];
        const predictedSpecies = speciesMap[result.prediction[0]];

        // Update UI
        predictionText.textContent = predictedSpecies;
        resultArea.classList.remove('hidden');
        
        // Scroll to result
        resultArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong. Please check if the backend is running.');
    } finally {
        btn.disabled = false;
        btnText.textContent = 'Analyze Features';
    }
});
