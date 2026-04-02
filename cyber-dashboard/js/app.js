document.addEventListener('DOMContentLoaded', () => {
    // Configurações globais do Chart.js
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.color = "#64748b";
    
    // Variáveis globais para os gráficos
    let trafficChartInstance = null;
    let threatsChartInstance = null;
    
    // URL da API PHP (Ajuste caso o servidor opere em porta ou pasta diferente)
    const API_URL = 'api/data.php';

    // Dispara a busca inicial
    fetchDashboardData();

    // Podemos atualizar os dados a cada 30 segundos
    setInterval(fetchDashboardData, 30000);

    // Função principal que orquestra a chamada de rede
    async function fetchDashboardData() {
        try {
            // Em ambiente real chamará a URL. 
            const response = await fetch(API_URL);
            
            if (!response.ok) {
                throw new Error("Erro na solicitação da API.");
            }
            
            const data = await response.json();
            
            updateMetrics(data.summary);
            updateTable(data.recent_logs);
            renderTrafficChart(data.traffic_data);
            renderThreatsChart(data.incidents_by_type);

            // Atualiza notificação com as anomalias
            document.getElementById('notification-badge').textContent = data.summary.anomalies_detected;

        } catch (error) {
            console.error("Erro ao carregar os dados:", error);
            // Em caso de erro local (ex: rodando index.html sem servidor), injetar mock para visualização
            loadMockData();
        }
    }

    // Atualiza os modais de resumo do topo
    function updateMetrics(summary) {
        // Usa efeito simples de counter iterativo para animação legal (Opcional, mas dá brilho)
        animateValue("metric-total-events", 0, summary.total_events, 1000);
        animateValue("metric-anomalies", 0, summary.anomalies_detected, 1000);
        document.getElementById('metric-threat-level').textContent = summary.threat_level;
        animateValue("metric-resolved", 0, summary.resolved_incidents, 1000);
    }

    // Anima a contagem de números progressivamente
    function animateValue(id, start, end, duration) {
        if (start === end) return;
        const obj = document.getElementById(id);
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // === [ MITIGAÇÃO CROSS-SITE SCRIPTING (DOM XSS) ] ===
    // Nunca podemos confiar cegamente nos logs de atacantes. Um log pode conter no IP algo como `<script>alert(1)</script>`.
    // Se inserirmos via innerHTML sem escapar, o navegador roda o vírus do atacante.
    function sanitize(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    // Preenche a tabela HTML a partir do JSON blindado
    function updateTable(logs) {
        const tbody = document.querySelector('#logsTable tbody');
        tbody.innerHTML = '';
        
        logs.forEach(log => {
            const tr = document.createElement('tr');
            
            // Formatando a classe cuidando para injetores não quebrarem o CSS
            let sevClass = sanitize(log.severity).toLowerCase().replace('í', 'i');
            
            // Todos os campos passíveis de injeção externa são sanitizados (Blindagem DOM)
            tr.innerHTML = `
                <td><strong>${sanitize(log.id)}</strong></td>
                <td>${sanitize(log.ip)}</td>
                <td>${sanitize(log.event)}</td>
                <td><span class="badge-status ${sevClass}">${sanitize(log.severity)}</span></td>
                <td>${sanitize(log.status)}</td>
                <td>${sanitize(log.time)}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    // Renderiza gráfico de linha de Tráfego (Chart.js)
    function renderTrafficChart(trafficData) {
        const ctx = document.getElementById('trafficChart').getContext('2d');
        
        // Destroi se já existia (Para não sobrepor em re-atualizações)
        if (trafficChartInstance) {
            trafficChartInstance.destroy();
        }

        // Gradiente do gráfico normal
        let gradientNormal = ctx.createLinearGradient(0, 0, 0, 400);
        gradientNormal.addColorStop(0, 'rgba(13, 110, 253, 0.2)');
        gradientNormal.addColorStop(1, 'rgba(13, 110, 253, 0)');

        // Gradiente das anomalias
        let gradientAnomalous = ctx.createLinearGradient(0, 0, 0, 400);
        gradientAnomalous.addColorStop(0, 'rgba(239, 68, 68, 0.2)');
        gradientAnomalous.addColorStop(1, 'rgba(239, 68, 68, 0)');

        trafficChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: trafficData.labels,
                datasets: [
                    {
                        label: 'Tráfego Normal (Req/s)',
                        data: trafficData.normal_traffic,
                        borderColor: '#0d6efd',
                        backgroundColor: gradientNormal,
                        borderWidth: 3,
                        pointBackgroundColor: '#ffffff',
                        pointBorderColor: '#0d6efd',
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Anomalias / Bloqueios',
                        data: trafficData.anomalous_traffic,
                        borderColor: '#ef4444',
                        backgroundColor: gradientAnomalous,
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        backgroundColor: '#1e293b',
                        padding: 12,
                        cornerRadius: 8,
                        titleFont: { size: 14, weight: 'normal' },
                    }
                },
                scales: {
                    x: {
                        grid: { display: false }
                    },
                    y: {
                        border: { display: false },
                        grid: { color: '#e2e8f0' }
                    }
                },
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
            }
        });
    }

    // Renderiza gráfico Doughnut para as Ameaças
    function renderThreatsChart(incidentTypes) {
        const ctx = document.getElementById('threatsChart').getContext('2d');
        
        if (threatsChartInstance) {
            threatsChartInstance.destroy();
        }

        const labels = Object.keys(incidentTypes);
        const dataVals = Object.values(incidentTypes);

        threatsChartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: dataVals,
                    backgroundColor: [
                        '#ef4444', // Red (Malware/Brute)
                        '#f59e0b', // Yellow (Phishing)
                        '#0d6efd', // Blue (DDoS)
                        '#8b5cf6'  // Purple (Others)
                    ],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    }
                },
                cutout: '75%', // Faz o prêmio visual ficar bem fino e estiloso
            }
        });
    }

    // Fallback Mock se a API falhar por estar testando o HTML diretamente
    function loadMockData() {
        console.warn("Utilizando Mock Local para demonstração UI (O PHP backend parece inativo).");
        const mock = {
            summary: {
                total_events: 14230, anomalies_detected: 84, threat_level: 'Moderado', resolved_incidents: 79
            },
            traffic_data: {
                labels: ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00'],
                normal_traffic: [120, 190, 300, 500, 200, 300, 250],
                anomalous_traffic: [5, 12, 10, 85, 20, 15, 10]
            },
            incidents_by_type: { Malware: 30, Phishing: 45, DDoS: 12, 'Brute Force': 95 },
            recent_logs: [
                {id: 'LOG-1029', ip: '192.168.1.105', event: 'Tentativa de Login Falha', severity: 'Alta', status: 'Bloqueado', time: '2 min atrás'},
                {id: 'LOG-1028', ip: '203.0.113.44', event: 'Pico Anormal de Tráfego HTTP', severity: 'Crítica', status: 'Em Análise', time: '15 min atrás'},
                {id: 'LOG-1027', ip: '10.0.0.8', event: 'Acesso Concedido (Root)', severity: 'Baixa', status: 'Concedido', time: '1 hora atrás'}
            ]
        };
        updateMetrics(mock.summary);
        updateTable(mock.recent_logs);
        renderTrafficChart(mock.traffic_data);
        renderThreatsChart(mock.incidents_by_type);
        document.getElementById('notification-badge').textContent = mock.summary.anomalies_detected;
    }

    // === [ SISTEMA DE NAVEGAÇÃO SPA (Single Page Application) ] ===
    // Prevenção de prototype pollution: As chaves permitidas são rigidamente checadas e não injetáveis vindo da URL
    const menuItems = document.querySelectorAll('.menu-item');
    const sections = document.querySelectorAll('.content-section');

    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault(); // Evita o recarregamento na URL 

            // 1. Remove classe active de todos os menus
            menuItems.forEach(nav => nav.classList.remove('active'));
            
            // 2. Oculta todas as seções
            sections.forEach(sec => {
                sec.classList.remove('active');
                sec.classList.add('hidden');
            });

            // 3. Ativa o menu selecionado e a seção correspondente
            item.classList.add('active');
            const targetId = item.getAttribute('data-target');
            
            // Segurança: Garantir que o alvo sempre existe e evitar Insecure Object Reference manipulado no HTML
            const targetSection = document.getElementById(targetId);
            if(targetSection && targetSection.classList.contains('content-section')) {
                targetSection.classList.remove('hidden');
                targetSection.classList.add('active');
            }
        });
    });
});
