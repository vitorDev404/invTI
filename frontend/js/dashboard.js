async function carregarDashboard() {
    try {
        const stats = await apiRequest("/stats/totais");

        document.getElementById("cardDispositivos").innerText = stats.dispositivos;
        document.getElementById("cardRacks").innerText = stats.racks;
        document.getElementById("cardImpressoras").innerText = stats.impressoras;
        document.getElementById("cardCPUs").innerText = stats.cpus;
        document.getElementById("cardItensCPU").innerText = stats.itens_cpu;

    } catch (error) {
        console.error("Erro carregando dashboard:", error);
        alert("Erro ao carregar estatísticas!");
    }
}
