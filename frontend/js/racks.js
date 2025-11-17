// racks.js - paginação + CRUD
const LIMIT_RACKS = 10;
let paginaRacks = 1;

async function carregarRacks(page = 1) {
    paginaRacks = page;
    try {
        const resp = await apiRequest(`/racks?page=${page}&limit=${LIMIT_RACKS}`);
        const dados = resp.dados || [];
        const tbody = document.getElementById("tabela-racks");
        tbody.innerHTML = "";

        dados.forEach(r => {
            tbody.innerHTML += `
                <tr>
                    <td>${r.id}</td>
                    <td>${r.patrimonio}</td>
                    <td>${r.rack}</td>
                    <td>${r.voltagem}</td>
                    <td>
                        <button onclick="abrirModalEditarRack(${r.id})">Editar</button>
                        <button onclick="deletarRack(${r.id})">Excluir</button>
                    </td>
                </tr>
            `;
        });

        criarPaginacao("paginacao-racks", resp.pagina, resp.total_paginas, carregarRacks);
    } catch (e) {
        console.error("Erro carregar racks:", e);
        alert("Erro ao carregar racks!");
    }
}

async function criarRack() {
    try {
        await apiRequest("/racks", "POST", {
            patrimonio: document.getElementById("patrimonioCriar").value,
            rack: document.getElementById("nomeCriar").value,
            voltagem: document.getElementById("voltagemCriar").value
        });
        fecharModalCriar();
        carregarRacks(paginaRacks);
    } catch (e) {
        alert("Erro ao criar rack: " + e.message);
    }
}

async function deletarRack(id) {
    if (!confirm("Confirmar exclusão do rack?")) return;
    try {
        await apiRequest(`/racks/${id}`, "DELETE");
        carregarRacks(paginaRacks);
    } catch (e) {
        alert("Erro ao deletar rack: " + e.message);
    }
}

async function abrirModalEditarRack(id) {
    try {
        const item = await apiRequest(`/racks/${id}`);
        document.getElementById("idEditar").value = item.id;
        document.getElementById("patrimonioEditar").value = item.patrimonio;
        document.getElementById("nomeEditar").value = item.rack;
        document.getElementById("voltagemEditar").value = item.voltagem;
        document.getElementById("modalEditar").style.display = "flex";
    } catch (e) {
        alert("Erro ao buscar rack: " + e.message);
    }
}

async function salvarEdicaoRack() {
    const id = document.getElementById("idEditar").value;
    try {
        await apiRequest(`/racks/${id}`, "PUT", {
            patrimonio: document.getElementById("patrimonioEditar").value,
            rack: document.getElementById("nomeEditar").value,
            voltagem: document.getElementById("voltagemEditar").value
        });
        fecharModalEditar();
        carregarRacks(paginaRacks);
    } catch (e) {
        alert("Erro ao salvar edição: " + e.message);
    }
}

window.addEventListener("load", () => carregarRacks(1));
function abrirModalCriacao() {
    const modal = document.getElementById("modalCriar");
    if (modal) modal.style.display = "flex";
}

function fecharModalCriar() {
    const modal = document.getElementById("modalCriar");
    if (modal) modal.style.display = "none";
}

function abrirModalEditar() {
    const modal = document.getElementById("modalEditar");
    if (modal) modal.style.display = "flex";
}

function fecharModalEditar() {
    const modal = document.getElementById("modalEditar");
    if (modal) modal.style.display = "none";
}