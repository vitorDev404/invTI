// cpu_itens.js - paginação + CRUD para itens de uma CPU específica
const LIMIT_ITENS = 10;
let paginaItens = 1;
let cpuId = null;

function obterCpuIdURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("cpu_id");
}

async function carregarItensCPU(page = 1) {
    paginaItens = page;
    cpuId = obterCpuIdURL();

    if (!cpuId) {
        alert("Nenhuma CPU selecionada!");
        window.location.href = "cpus.html";
        return;
    }

    document.getElementById("titulo-pagina").innerText = `Itens da CPU #${cpuId}`;

    try {
        const resp = await apiRequest(`/cpu_itens/cpu/${cpuId}?page=${page}&limit=${LIMIT_ITENS}`);
        const dados = resp.dados || [];
        const tbody = document.getElementById("tabela-itens");
        tbody.innerHTML = "";

        dados.forEach(item => {
            tbody.innerHTML += `
                <tr>
                    <td>${item.id}</td>
                    <td>${item.tipo}</td>
                    <td>${item.patrimonio}</td>
                    <td>${item.descricao || ""}</td>
                    <td>
                        <button onclick="abrirModalEditarItem(${item.id})">Editar</button>
                        <button onclick="deletarItem(${item.id})">Excluir</button>
                    </td>
                </tr>
            `;
        });

        criarPaginacao("paginacao-itens", resp.pagina, resp.total_paginas, carregarItensCPU);
    } catch (e) {
        console.error("Erro carregar itens:", e);
        alert("Erro ao carregar itens da CPU!");
    }
}

async function criarItem() {
    try {
        await apiRequest("/cpu_itens", "POST", {
            cpu_id: cpuId,
            tipo: document.getElementById("tipoCriar").value,
            patrimonio: document.getElementById("patrimonioCriar").value,
            descricao: document.getElementById("descricaoCriar").value
        });
        fecharModalCriar();
        carregarItensCPU(paginaItens);
    } catch (e) {
        alert("Erro ao criar item: " + e.message);
    }
}

async function deletarItem(id) {
    if (!confirm("Confirmar exclusão do item?")) return;
    try {
        await apiRequest(`/cpu_itens/${id}`, "DELETE");
        carregarItensCPU(paginaItens);
    } catch (e) {
        alert("Erro ao deletar item: " + e.message);
    }
}

async function abrirModalEditarItem(id) {
    try {
        const item = await apiRequest(`/cpu_itens/${id}`);
        document.getElementById("idEditar").value = item.id;
        document.getElementById("tipoEditar").value = item.tipo;
        document.getElementById("patrimonioEditar").value = item.patrimonio;
        document.getElementById("descricaoEditar").value = item.descricao || "";
        document.getElementById("modalEditar").style.display = "flex";
    } catch (e) {
        alert("Erro ao buscar item: " + e.message);
    }
}

async function salvarEdicaoItem() {
    const id = document.getElementById("idEditar").value;
    try {
        await apiRequest(`/cpu_itens/${id}`, "PUT", {
            tipo: document.getElementById("tipoEditar").value,
            patrimonio: document.getElementById("patrimonioEditar").value,
            descricao: document.getElementById("descricaoEditar").value
        });
        fecharModalEditar();
        carregarItensCPU(paginaItens);
    } catch (e) {
        alert("Erro ao salvar item: " + e.message);
    }
}

window.addEventListener("load", () => carregarItensCPU(1));
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