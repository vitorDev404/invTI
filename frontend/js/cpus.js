// cpus.js - paginação + CRUD + abrir itens
const LIMIT_CPUS = 10;
let paginaCPUs = 1;

async function carregarCPUs(page = 1) {
    paginaCPUs = page;
    try {
        const resp = await apiRequest(`/cpus?page=${page}&limit=${LIMIT_CPUS}`);
        const dados = resp.dados || [];
        const tbody = document.getElementById("tabela-cpus");
        tbody.innerHTML = "";

        dados.forEach(cpu => {
            tbody.innerHTML += `
                <tr>
                    <td>${cpu.id}</td>
                    <td>${cpu.cpu_patrimonio}</td>
                    <td>${cpu.hostname}</td>
                    <td>${cpu.setor}</td>
                    <td>${cpu.impressora}</td>
                    <td>${cpu.ip}</td>
                    <td>${cpu.local}</td>
                    <td>
                        <button onclick="abrirItensCPU(${cpu.id})">Itens</button>
                        <button onclick="abrirModalEditarCPU(${cpu.id})">Editar</button>
                        <button onclick="deletarCPU(${cpu.id})">Excluir</button>
                    </td>
                </tr>
            `;
        });

        criarPaginacao("paginacao-cpus", resp.pagina, resp.total_paginas, carregarCPUs);
    } catch (e) {
        console.error("Erro carregar cpus:", e);
        alert("Erro ao carregar CPUs!");
    }
}

function abrirItensCPU(cpu_id) {
    window.location.href = `cpu_itens.html?cpu_id=${cpu_id}`;
}

async function criarCPU() {
    try {
        await apiRequest("/cpus", "POST", {
            cpu_patrimonio: document.getElementById("patrimonioCriar").value,
            hostname: document.getElementById("hostnameCriar").value,
            setor: document.getElementById("setorCriar").value,
            impressora: document.getElementById("impressoraCriar").value,
            ip: document.getElementById("ipCriar").value,
            local: document.getElementById("localCriar").value
        });
        fecharModalCriar();
        carregarCPUs(paginaCPUs);
    } catch (e) {
        alert("Erro ao criar CPU: " + e.message);
    }
}

async function deletarCPU(id) {
    if (!confirm("Confirmar exclusão da CPU?")) return;
    try {
        await apiRequest(`/cpus/${id}`, "DELETE");
        carregarCPUs(paginaCPUs);
    } catch (e) {
        alert("Erro ao deletar CPU: " + e.message);
    }
}

async function abrirModalEditarCPU(id) {
    try {
        const cpu = await apiRequest(`/cpus/${id}`);
        document.getElementById("idEditar").value = cpu.id;
        document.getElementById("patrimonioEditar").value = cpu.cpu_patrimonio;
        document.getElementById("hostnameEditar").value = cpu.hostname;
        document.getElementById("setorEditar").value = cpu.setor;
        document.getElementById("impressoraEditar").value = cpu.impressora;
        document.getElementById("ipEditar").value = cpu.ip;
        document.getElementById("localEditar").value = cpu.local;
        document.getElementById("modalEditar").style.display = "flex";
    } catch (e) {
        alert("Erro ao buscar CPU: " + e.message);
    }
}

async function salvarEdicaoCPU() {
    const id = document.getElementById("idEditar").value;
    try {
        await apiRequest(`/cpus/${id}`, "PUT", {
            cpu_patrimonio: document.getElementById("patrimonioEditar").value,
            hostname: document.getElementById("hostnameEditar").value,
            setor: document.getElementById("setorEditar").value,
            impressora: document.getElementById("impressoraEditar").value,
            ip: document.getElementById("ipEditar").value,
            local: document.getElementById("localEditar").value
        });
        fecharModalEditar();
        carregarCPUs(paginaCPUs);
    } catch (e) {
        alert("Erro ao salvar CPU: " + e.message);
    }
}

window.addEventListener("load", () => carregarCPUs(1));
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