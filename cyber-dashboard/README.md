# CyberAnalytics - Dashboard

Um Dashboard Executivo leve, moderno (Vanilla JS/CSS) construído com foco primário em visualização de dados de cibersegurança e alta resiliência a ataques Front-end.

## Funcionalidades
- **SPA (Single Page Application)**: Navegação sem recarregamento.
- **Gráficos em Tempo Real**: Usando Chart.js com contadores progressivos.
- **Micro-interações e UI Glassmorphism (Branco)**.
- **Segurança Nível Sênior**:
  - `Content Security Policy (CSP)` embutido para barrar XSS.
  - Mitigação de `Magecart` isolando scripts via integridade.
  - Componentização segura sem injeção vulnerável no DOM.

## Como Instalar / Executar
1. Clone este repositório.
2. Como se trata de um frontend puramente JS e HTML, basta dar um duplo-clique no **`index.html`**. 

O sistema conta com um "Mock Fallback", gerando dados caso o banco de dados oficial (PHP) esteja ausente.

Se for operar via Backend oficial:
```bash
php -S localhost:8000
```
Acesse `http://localhost:8000`.
