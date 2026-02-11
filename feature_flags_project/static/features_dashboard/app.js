const API_URL = "/api/features/";

async function loadFeatures() {
    const tbody = document.querySelector("#featuresTable tbody");

    try {
        const res = await fetch(API_URL);

        if (!res.ok) {
            throw new Error('Error al cargar features');
        }

        const data = await res.json();

        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">No hay features todavía</td></tr>';
            return;
        }

        data.sort((a, b) => a.id - b.id);

        tbody.innerHTML = "";
        data.forEach(f => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${f.id}</td>
                <td>${f.name}</td>
                <td>${f.enabled ? 'Activo' : 'Inactivo'}</td>
                <td>
                    <button class="btn btn-sm ${f.enabled ? 'btn-secondary' : 'btn-success'}"
                            onclick="toggleFeature(${f.id}, ${f.enabled})">
                        ${f.enabled ? 'Desactivar' : 'Activar'}
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="4" class="text-center text-danger">Error: ${error.message}</td></tr>`;
        console.error('Error:', error);
    }
}

async function toggleFeature(id, currentValue) {
    try {
        const res = await fetch(`${API_URL}${id}/`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ enabled: !currentValue })
        });

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(errorText);
        }

        await loadFeatures();

    } catch (error) {
        alert("Error al actualizar: " + error.message);
        console.error('Error:', error);
    }
}

loadFeatures();
