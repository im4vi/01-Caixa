const API_URL = "http://localhost:8000/api/features/";

function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return cookieValue ? cookieValue.split('=')[1] : null;
}

async function loadFeatures() {
    const res = await fetch(API_URL, { credentials: "include" });
    const data = await res.json();

    const tbody = document.querySelector("#featuresTable tbody");
    tbody.innerHTML = "";

    data.forEach(f => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${f.id}</td>
            <td>${f.name}</td>
            <td>${f.enabled}</td>
            <td>
                <button onclick="toggleFeature(${f.id}, ${f.enabled})">
                    Toggle
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function toggleFeature(id, currentValue) {
    const newValue = !currentValue;
    const csrftoken = getCookie("csrftoken");

    const res = await fetch(`${API_URL}${id}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest"
        },
        credentials: "include",
        body: JSON.stringify({ enabled: newValue })
    });

    if (!res.ok) {
        const txt = await res.text();
        alert("PATCH Failed: " + txt);
    }

    loadFeatures();
}

loadFeatures();
