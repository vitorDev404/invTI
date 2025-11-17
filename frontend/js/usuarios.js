// usuarios.js - paginação + CRUD (admin)
const LIMIT_USUARIOS = 10;
let paginaUsuarios = 1;

async function carregarUsuarios(page = 1) {
    paginaUsuarios = page;
    try {
        const resp = await apiRequest(`/usuarios?page=${page}&limit=${LIMIT_USUARIOS}`);
        const dados = resp.dados || [];
        const tbody = document.getElementById("tabela-usuarios");
        tbody.innerHTML = "";

        dados.forEach(u => {
            // badge visual -> pode ser substituído por HTML com classes se quiser estilos
            const badge = u.nivel_acesso === "admin" ? `<span class="badge badge-admin">Admin</span>` : `<span class="badge badge-user">Usuário</span>`;
            tbody.innerHTML += `
                <tr>
                    <td>${u.id}</td>
                    <td>${u.nome}</td>
                    <td>${u.email}</td>
                    <td>${badge}</td>
                    <td>
                        <button onclick="abrirModalEditarUsuario(${u.id})">Editar</button>
                        <button onclick="deletarUsuario(${u.id}, '${u.nivel_acesso}')">Excluir</button>
                        <button onclick="resetarSenhaConfirm(${u.id})">Redefinir senha</button>
                    </td>
                </tr>
            `;
        });

        criarPaginacao("paginacao-usuarios", resp.pagina, resp.total_paginas, carregarUsuarios);
    } catch (e) {
        console.error("Erro carregar usuarios:", e);
        alert("Erro ao carregar usuários!");
    }
}

async function criarUsuario() {
    try {
        await apiRequest("/usuarios", "POST", {
            nome: document.getElementById("nomeCriar").value,
            email: document.getElementById("emailCriar").value,
            senha: document.getElementById("senhaCriar").value,
            nivel_acesso: document.getElementById("nivelCriar").value
        });
        fecharModalCriar();
        carregarUsuarios(paginaUsuarios);
    } catch (e) {
        alert("Erro ao criar usuário: " + e.message);
    }
}

async function deletarUsuario(id, nivel) {
    if (nivel === "admin") {
        if (!confirm("⚠ Este usuário é ADMIN! Tem certeza absoluta que deseja removê-lo?")) return;
    } else {
        if (!confirm("Confirmar exclusão do usuário?")) return;
    }

    try {
        await apiRequest(`/usuarios/${id}`, "DELETE");
        carregarUsuarios(paginaUsuarios);
    } catch (e) {
        alert("Erro ao deletar usuário: " + e.message);
    }
}

async function abrirModalEditarUsuario(id) {
    try {
        const u = await apiRequest(`/usuarios/${id}`);
        document.getElementById("idEditar").value = u.id;
        document.getElementById("nomeEditar").value = u.nome;
        document.getElementById("emailEditar").value = u.email;
        document.getElementById("nivelEditar").value = u.nivel_acesso;
        document.getElementById("modalEditar").style.display = "flex";
    } catch (e) {
        alert("Erro ao buscar usuário: " + e.message);
    }
}

async function salvarEdicaoUsuario() {
    const id = document.getElementById("idEditar").value;
    try {
        await apiRequest(`/usuarios/${id}`, "PUT", {
            nome: document.getElementById("nomeEditar").value,
            email: document.getElementById("emailEditar").value,
            senha: document.getElementById("senhaEditar").value || null,
            nivel_acesso: document.getElementById("nivelEditar").value
        });
        fecharModalEditar();
        carregarUsuarios(paginaUsuarios);
    } catch (e) {
        alert("Erro ao salvar usuário: " + e.message);
    }
}

// reset senha helper (calls auth route)
async function resetarSenhaConfirm(id) {
    if (!confirm("Redefinir senha deste usuário para '123456'?")) return;
    try {
        await apiRequest(`/auth/reset_senha/${id}`, "POST");
        alert("Senha redefinida para '123456'!");
    } catch (e) {
        alert("Erro ao redefinir senha: " + e.message);
    }
}

window.addEventListener("load", () => carregarUsuarios(1));
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