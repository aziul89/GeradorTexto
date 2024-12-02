document.getElementById('textForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    document.getElementById('loadingMessage').style.display = 'block';

    const prompt = document.getElementById('prompt').value;
    const maxLength = document.getElementById('maxLength').value;

    try {
        const response = await fetch('http://localhost:5000/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                max_length: parseInt(maxLength),
            }),
        });

        const data = await response.json();

        document.getElementById('loadingMessage').style.display = 'none';

        if (data.generated_text) {
            document.getElementById('generatedText').innerText = data.generated_text;
        } else {
            document.getElementById('generatedText').innerText = "Erro: " + (data.error || "Ocorreu um erro inesperado.");
        }
    } catch (error) {
        document.getElementById('loadingMessage').style.display = 'none';
        document.getElementById('generatedText').innerText = "Erro: " + error.message;
    }
});

