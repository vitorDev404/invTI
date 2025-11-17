function criarPaginacao(containerId, paginaAtual, totalPaginas, aoClicar) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    if (totalPaginas <= 1) return;

    function botao(numero, texto = null) {
        const btn = document.createElement("button");
        btn.innerText = texto || numero;
        btn.className = "btn-page";
        if (numero === paginaAtual) btn.classList.add("active");
        btn.onclick = () => aoClicar(numero);
        return btn;
    }

    if (paginaAtual > 1) container.appendChild(botao(paginaAtual - 1, "«"));

    // mostra páginas com compactação
    const maxMostrar = 7;
    let start = Math.max(1, paginaAtual - Math.floor(maxMostrar / 2));
    let end = Math.min(totalPaginas, start + maxMostrar - 1);
    if (end - start + 1 < maxMostrar) start = Math.max(1, end - maxMostrar + 1);

    if (start > 1) {
        container.appendChild(botao(1));
        if (start > 2) {
            const span = document.createElement("span");
            span.innerText = "...";
            span.className = "dots";
            container.appendChild(span);
        }
    }

    for (let i = start; i <= end; i++) {
        container.appendChild(botao(i));
    }

    if (end < totalPaginas) {
        if (end < totalPaginas - 1) {
            const span = document.createElement("span");
            span.innerText = "...";
            span.className = "dots";
            container.appendChild(span);
        }
        container.appendChild(botao(totalPaginas));
    }

    if (paginaAtual < totalPaginas) container.appendChild(botao(paginaAtual + 1, "»"));
}
