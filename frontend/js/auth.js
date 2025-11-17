async function login() {
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    const result = await apiRequest("/auth/login", "POST", {
        email,
        senha
    });

    if (result.token) {
        localStorage.setItem("token", result.token);
        localStorage.setItem("usuario", JSON.stringify(result.usuario));
        window.location.href = "dashboard.html";
    } else {
        alert("Credenciais inválidas.");
    }
}

function verificarLogin() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "index.html";
        document.getElementById("usuario-logado").innerText =
    `🔐 Logado como: ${usuario.email} (${usuario.nivel_acesso})`;
    return;
    }

    const usuario = JSON.parse(localStorage.getItem("usuario"));

    if (!usuario) {
        logout();
        return;
    }

    if (usuario.nivel_acesso !== "admin") {
        document.querySelectorAll(".admin-only").forEach(el => {
            el.style.display = "none";
        });
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    window.location.href = "index.html";
}
