// dispositivos.js - paginação + CRUD
const LIMIT_DISPOSITIVOS = 10;
let paginaDispositivos = 1;

async function carregarDispositivos(page = 1) {
    paginaDispositivos = page;
    try {
        const resp = await apiRequest(`/dispositivos?page=${page}&limit=${LIMIT_DISPOSITIVOS}`);
        const dados = resp.dados || [];
        const tbody = document.getElementById("tabela-dispositivos");
        tbody.innerHTML = "";

        dados.forEach(dis => {
            tbody.innerHTML += `
                <tr>
                    <td>${dis.id}</td>
                    <td>${dis.patrimonio}</td>
                    <td>${dis.modelo}</td>
                    <td>${dis.usuario}</td>
                    <td>${dis.cargo_unidade_setor}</td>
                    <td>
                        <button onclick="abrirModalEditarDispositivo(${dis.id})">Editar</button>
                        <button onclick="deletarDispositivo(${dis.id})">Excluir</button>
                    </td>
                </tr>
            `;
        });

        criarPaginacao("paginacao-dispositivos", resp.pagina, resp.total_paginas, carregarDispositivos);
    } catch (e) {
        console.error("Erro carregar dispositivos:", e);
        alert("Erro ao carregar dispositivos!");
    }
}

// CREATE
async function criarDispositivo() {
    try {
        await apiRequest("/dispositivos", "POST", {
            patrimonio: document.getElementById("patrimonioCriar").value,
            modelo: document.getElementById("modeloCriar").value,
            usuario: document.getElementById("usuarioCriar").value,
            cargo_unidade_setor: document.getElementById("cargoCriar").value
        });
        fecharModalCriar();
        carregarDispositivos(paginaDispositivos);
    } catch (e) {
        alert("Erro ao criar dispositivo: " + e.message);
    }
}

// DELETE
async function deletarDispositivo(id) {
    if (!confirm("Confirmar exclusão?")) return;
    try {
        await apiRequest(`/dispositivos/${id}`, "DELETE");
        carregarDispositivos(paginaDispositivos);
    } catch (e) {
        alert("Erro ao deletar: " + e.message);
    }
}

// EDIT FLOW - fetch item then fill modal
async function abrirModalEditarDispositivo(id) {
    try {
        const item = await apiRequest(`/dispositivos/${id}`);
        document.getElementById("idEditar").value = item.id;
        document.getElementById("patrimonioEditar").value = item.patrimonio;
        document.getElementById("modeloEditar").value = item.modelo;
        document.getElementById("usuarioEditar").value = item.usuario;
        document.getElementById("cargoEditar").value = item.cargo_unidade_setor;
        document.getElementById("modalEditar").style.display = "flex";
    } catch (e) {
        alert("Erro ao buscar dispositivo: " + e.message);
    }
}

async function salvarEdicaoDispositivo() {
    const id = document.getElementById("idEditar").value;
    try {
        await apiRequest(`/dispositivos/${id}`, "PUT", {
            patrimonio: document.getElementById("patrimonioEditar").value,
            modelo: document.getElementById("modeloEditar").value,
            usuario: document.getElementById("usuarioEditar").value,
            cargo_unidade_setor: document.getElementById("cargoEditar").value
        });
        fecharModalEditar();
        carregarDispositivos(paginaDispositivos);
    } catch (e) {
        alert("Erro ao salvar edição: " + e.message);
    }
}

// ensure initial load
window.addEventListener("load", () => carregarDispositivos(1));
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