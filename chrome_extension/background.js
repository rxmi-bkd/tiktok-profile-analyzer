chrome
    .runtime
    .onMessage
    .addListener((message) => {
            const options = {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(message)
            }

            fetch('http://localhost:5000/', options);
        }
    );
