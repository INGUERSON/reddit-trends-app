<?php
// === [ CAMADA DE SEGURANÇA E HEADERS FULLSTACK ] ===
// Bloqueia tentativas de Clickjacking (impede o site de ser colocado num iframe)
header("X-Frame-Options: DENY");
// Força o navegador a respeitar o mime-type, bloqueando MIME sniffing
header("X-Content-Type-Options: nosniff");
// Habilita filtro XSS interno do navegador
header("X-XSS-Protection: 1; mode=block");
// Envia o tipo de conteúdo apenas via UTF-8
header('Content-Type: application/json; charset=UTF-8');

// [CORREÇÃO DE VULNERABILIDADE CORS]:
// O uso de `Access-Control-Allow-Origin: *` permitia que qualquer site na internet puxasse seus dados.
// Alterado para permitir apenas o front-end autorizado (Ex: localhost em dev).
// Em Produção você colocaria seu domínio: header("Access-Control-Allow-Origin: https://meusistema.com");
$allowed_origin = 'http://localhost:8000'; // Insira o IP real em produção
header("Access-Control-Allow-Origin: " . $allowed_origin);
header("Access-Control-Allow-Methods: GET"); // Ninguém pode enviar POSTS, PUTS ou DELETES maliciosos nesta rota


// Simulação de processamento de dados e análise de logs
// Em um caso de uso real, você conectaria aqui a um banco de dados
// ou analisaria arquivos .log em tempo real.

$data = [
    'summary' => [
        'total_events' => 14230,
        'anomalies_detected' => 84,
        'threat_level' => 'Moderado',
        'resolved_incidents' => 79
    ],
    'traffic_data' => [
        'labels' => ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00'],
        'normal_traffic' => [120, 190, 300, 500, 200, 300, 250],
        'anomalous_traffic' => [5, 12, 10, 85, 20, 15, 10]
    ],
    'incidents_by_type' => [
        'Malware' => 30,
        'Phishing' => 45,
        'DDoS' => 12,
        'Brute Force' => 95
    ],
    'recent_logs' => [
        ['id' => 'LOG-1029', 'ip' => '192.168.1.105', 'event' => 'Tentativa de Login Falha (Admin)', 'severity' => 'Alta', 'status' => 'Bloqueado', 'time' => '2 min atrás'],
        ['id' => 'LOG-1028', 'ip' => '203.0.113.44', 'event' => 'Pico Anormal de Tráfego HTTP', 'severity' => 'Crítica', 'status' => 'Em Análise', 'time' => '15 min atrás'],
        ['id' => 'LOG-1027', 'ip' => '10.0.0.8', 'event' => 'Acesso Concedido (Root)', 'severity' => 'Baixa', 'status' => 'Concedido', 'time' => '1 hora atrás'],
        ['id' => 'LOG-1026', 'ip' => '198.51.100.12', 'event' => 'Port Scan Detectado', 'severity' => 'Média', 'status' => 'Bloqueado', 'time' => '3 horas atrás']
    ]
];

echo json_encode($data);
?>
