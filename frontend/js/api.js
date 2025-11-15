const API_URL = "http://127.0.0.1:5000";

async function apiRequest(endpoint, method = "GET", body = null) {
    const token = localStorage.getItem("token");

    const options = {
        method,
        headers: {
            "Content-Type": "application/json",
        }
    };

    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }

    if (body) {
        options.body = JSON.stringify(body);
    }

    // Monta a URL *exatamente* com o endpoint que você passar (sem alterar barras)
    const url = API_URL + endpoint;

    console.log("🚀 fetch ->", method, url, body ? body : "");

    try {
        const response = await fetch(url, options);
        // tenta ler texto para mensagens de erro mais claras
        const text = await response.text();
        let data = null;
        try { data = text ? JSON.parse(text) : null } catch(e) { data = text; }

        if (!response.ok) {
            // mostra info útil no console
            console.error("API ERRO:", response.status, response.statusText, data);
            throw new Error((data && (data.erro || data.message || data.mensagem)) || `HTTP ${response.status}`);
        }
        return data;
    } catch (err) {
        console.error("FETCH FAILED:", err);
        // lança erro para o frontend exibir
        throw new Error(err.message || "Failed to fetch");
    }
}
