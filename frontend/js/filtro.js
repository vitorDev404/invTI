function aplicarFiltro(inputId, tabelaId) {
    const termo = document.getElementById(inputId).value.toLowerCase();
    const linhas = document.querySelectorAll(`#${tabelaId} tr`);
    linhas.forEach(linha => {
        const texto = linha.innerText.toLowerCase();
        linha.style.display = texto.includes(termo) ? "" : "none";
    });
}
