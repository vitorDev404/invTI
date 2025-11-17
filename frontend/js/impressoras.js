// impressoras.js - paginação + CRUD
const LIMIT_IMPRESSORAS = 10;
let paginaImpressoras = 1;

async function carregarImpressoras(page = 1) {
    paginaImpressoras = page;
    try {
        const resp = await apiRequest(`/impressoras?page=${page}&limit=${LIMIT_IMPRESSORAS}`);
        const dados = resp.dados || [];
        const tbody = document.getElementById("tabela-impressoras");
        tbody.innerHTML = "";

        dados.forEach(imp => {
            tbody.innerHTML += `
                <tr>
                    <td>${imp.id}</td>
                    <td>${imp.modelo}</td>
                    <td>${imp.unidade}</td>
                    <td>${imp.local}</td>
                    <td>${imp.numero_serie}</td>
                    <td>${imp.ip_equipamento}</td>
                    <td>${imp.nome_impressora_servidor}</td>
                    <td>${imp.ndd}</td>
                    <td>${imp.mac}</td>
                    <td>${imp.observacoes || ""}</td>
                    <td>
                        <button onclick="abrirModalEditarImpressora(${imp.id})">Editar</button>
                        <button onclick="deletarImpressora(${imp.id})">Excluir</button>
                    </td>
                </tr>
            `;
        });

        criarPaginacao("paginacao-impressoras", resp.pagina, resp.total_paginas, carregarImpressoras);
    } catch (e) {
        console.error("Erro carregar impressoras:", e);
        alert("Erro ao carregar impressoras!");
    }
}

async function criarImpressora() {
    try {
        await apiRequest("/impressoras", "POST", {
            modelo: document.getElementById("modeloCriar").value,
            unidade: document.getElementById("unidadeCriar").value,
            local: document.getElementById("localCriar").value,
            numero_serie: document.getElementById("numeroCriar").value,
            ip_equipamento: document.getElementById("ipCriar").value,
            nome_impressora_servidor: document.getElementById("nomeServidorCriar").value,
            ndd: document.getElementById("nddCriar").value,
            mac: document.getElementById("macCriar").value,
            observacoes: document.getElementById("obsCriar").value
        });
        fecharModalCriar();
        carregarImpressoras(paginaImpressoras);
    } catch (e) {
        alert("Erro ao criar impressora: " + e.message);
    }
}

async function deletarImpressora(id) {
    if (!confirm("Confirmar exclusão da impressora?")) return;
    try {
        await apiRequest(`/impressoras/${id}`, "DELETE");
        carregarImpressoras(paginaImpressoras);
    } catch (e) {
        alert("Erro ao deletar impressora: " + e.message);
    }
}

async function abrirModalEditarImpressora(id) {
    try {
        const imp = await apiRequest(`/impressoras/${id}`);
        document.getElementById("idEditar").value = imp.id;
        document.getElementById("modeloEditar").value = imp.modelo;
        document.getElementById("unidadeEditar").value = imp.unidade;
        document.getElementById("localEditar").value = imp.local;
        document.getElementById("numeroEditar").value = imp.numero_serie;
        document.getElementById("ipEditar").value = imp.ip_equipamento;
        document.getElementById("nomeServidorEditar").value = imp.nome_impressora_servidor;
        document.getElementById("nddEditar").value = imp.ndd;
        document.getElementById("macEditar").value = imp.mac;
        document.getElementById("obsEditar").value = imp.observacoes || "";
        document.getElementById("modalEditar").style.display = "flex";
    } catch (e) {
        alert("Erro ao buscar impressora: " + e.message);
    }
}

async function salvarEdicaoImpressora() {
    const id = document.getElementById("idEditar").value;
    try {
        await apiRequest(`/impressoras/${id}`, "PUT", {
            modelo: document.getElementById("modeloEditar").value,
            unidade: document.getElementById("unidadeEditar").value,
            local: document.getElementById("localEditar").value,
            numero_serie: document.getElementById("numeroEditar").value,
            ip_equipamento: document.getElementById("ipEditar").value,
            nome_impressora_servidor: document.getElementById("nomeServidorEditar").value,
            ndd: document.getElementById("nddEditar").value,
            mac: document.getElementById("macEditar").value,
            observacoes: document.getElementById("obsEditar").value
        });
        fecharModalEditar();
        carregarImpressoras(paginaImpressoras);
    } catch (e) {
        alert("Erro ao salvar impressora: " + e.message);
    }
}

window.addEventListener("load", () => carregarImpressoras(1));
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