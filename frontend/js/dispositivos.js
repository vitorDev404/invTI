async function carregarDispositivos() {
    try {
        const dispositivos = await apiRequest("/dispositivos/");
        const tbody = document.getElementById("tabela-dispositivos");

        tbody.innerHTML = "";

        dispositivos.forEach(dis => {
            tbody.innerHTML += `
                <tr>
                    <td>${dis.id}</td>
                    <td>${dis.patrimonio}</td>
                    <td>${dis.modelo}</td>
                    <td>${dis.usuario}</td>
                    <td>${dis.cargo_unidade_setor}</td>
                    <td>
                        <button onclick="deletarDispositivo(${dis.id})">🗑️</button>
                    </td>
                </tr>
            `;
        });

    } catch (error) {
        console.error("Erro ao carregar dispositivos:", error);
    }
}


function abrirModalCriar() {
    document.getElementById("modalCriar").style.display = "flex";
}

function fecharModalCriar() {
    document.getElementById("modalCriar").style.display = "none";
}

async function criarDispositivo() {
    const patrimonio = document.getElementById("patrimonioCriar").value;
    const modelo = document.getElementById("modeloCriar").value;
    const usuario = document.getElementById("usuarioCriar").value;
    const setor = document.getElementById("cargoCriar").value;

    try {
        await apiRequest("/dispositivos/", "POST", {
            patrimonio,
            modelo,
            usuario,
            cargo_unidade_setor: setor
        });

        fecharModalCriar();
        carregarDispositivos();

    } catch (error) {
        alert("Erro ao criar dispositivo: " + error.message);
    }
}