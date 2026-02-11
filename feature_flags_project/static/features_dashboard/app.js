const API_URL = "/api/features/";

function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return cookieValue ? cookieValue.split('=')[1] : null;
}

async function loadFeatures() {
    try {
        const res = await fetch(API_URL);
        const data = await res.json();

        const tbody = document.querySelector("#featuresTable tbody");
        tbody.innerHTML = "";

        data.forEach(f => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${f.id}</td>
                <td>${f.name}</td>
                <td>${f.enabled ? '✓' : '✗'}</td>
                <td>
                    <button onclick="toggleFeature(${f.id}, ${f.enabled})">
                        Toggle
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error:', error);
        alert('Error cargando features: ' + error.message);
    }
}

async function toggleFeature(id, currentValue) {
    const newValue = !currentValue;
    const csrftoken = getCookie("csrftoken");

    try {
        const res = await fetch(`${API_URL}${id}/`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({ enabled: newValue })
        });

        if (!res.ok) {
            const txt = await res.text();
            alert("Error: " + txt);
        } else {
            loadFeatures();
        }
    } catch (error) {
        alert("Error: " + error.message);
    }
}

loadFeatures();
