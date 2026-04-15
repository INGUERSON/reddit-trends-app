# Guia Completo de Desenvolvimento Front-End para Estudantes de ADS (Análise e Desenvolvimento de Sistemas)

Este material foi construído para guiá-lo desde os fundamentos da web até a construção de aplicações modernas com React, focado nas exigências do mercado para desenvolvedores Front-End.

---

## Módulo 1: Fundamentos da Web (HTML e CSS)

Antes de qualquer framework, é vital dominar as bases da web. A estrutura e a estilização são o coração de qualquer site.

### 1.1. HTML5 (Estrutura e Semântica)
O HTML é a base de tudo. Concentre-se em aprender a semântica correta (usar as tags `header`, `nav`, `main`, `article`, `footer`, etc., em vez de apenas `div`), acessibilidade e formulários.

### 1.2. CSS3 (Estilização e Layout)
O CSS dá vida à estrutura. 
- **Conceitos Críticos:** Box Model (Margem, Borda, Padding, Conteúdo), Seletores, Especificidade.
- **Sistemas de Layout:** Flexbox (essencial para alinhamento e layouts unidimensionais) e CSS Grid (para layouts bidimensionais complexos).
- **Responsividade:** Media Queries (`@media`) e abordagens Mobile First.

### Materiais Recomendados (Iniciantes):
*   **[freeCodeCamp](https://www.freecodecamp.org/portuguese/):** Currículo prático e gratuito, comece pela certificação de "Design da Web Responsivo".
*   **[MDN Web Docs (Mozilla)](https://developer.mozilla.org/pt-BR/):** A documentação oficial da Web. Excelente para consultar como funcionam as tags HTML e propriedades CSS.
*   **Canal Curso em Vídeo (Prof. Gustavo Guanabara):** O curso de HTML5 e CSS3 é um dos mais didáticos em língua portuguesa para absolute beginners.

---

## Módulo 2: O Cérebro da Operação (JavaScript)

JavaScript é o que permite que a web seja dinâmica e interativa. Não pule para o React sem antes dominar o JavaScript puro (Vanilla JS).

### Conceitos Essenciais que devem ser dominados:
1.  **Fundamentos:** Variáveis (`let`, `const`), Tipos de Dados, Operadores, Estruturas de Controle (`if/else`, `switch`, loops `for` e `while`).
2.  **Funções:** Declarações, Expressões, e principalmente **Arrow Functions** (muito usadas no React).
3.  **Estruturas de Dados:** Arrays e Objetos. Domine métodos de iteração modernos como `.map()`, `.filter()`, e `.reduce()`.
4.  **Manipulação do DOM:** Como selecionar elementos HTML (`querySelector`), alterar seus estilos, conteúdos e reagir a eventos (`addEventListener`).
5.  **Assincronismo:** Promises, `async` / `await`, e consumo de APIs externas (usando `fetch`).
6.  **ES6+:** Desestruturação (Destructuring), Spread/Rest Operators e Template Literals.

### Materiais Recomendados (JavaScript):
*   **[JavaScript.info](https://javascript.info/):** O tutorial mais profundo de JavaScript da internet.
*   **[Origamid](https://www.origamid.com/):** O curso de JavaScript Completo ES6+ deles é uma fortíssima referência no Brasil.
*   **Canal do YouTube Hora de Codar:** Ótimos vídeos curtos e projetos longos usando apenas HTML, CSS e JavaScript puro.

---

## Módulo 3: O Padrão de Mercado (React.js)

O React é hoje a biblioteca de interfaces de usuário mais requisitada no mercado de trabalho.

### Por que aprender React?
Ele permite a criação de interfaces modulares (Componentes) e introduz o conceito de reatividade e estado, atualizando apenas as partes da interface que realmente mudaram (Virtual DOM).

### O que estudar em React:
1.  **Fundamentos de Componentização:** Como quebrar uma página em partes menores e reutilizáveis (Componentes Funcionais).
2.  **JSX:** A sintaxe que mistura HTML com JavaScript.
3.  **Props (Propriedades):** Como passar dados de um componente "Pai" para um "Filho".
4.  **State (Estado) e o Hook `useState`:** Como gerenciar dados que mudam internamente em um componente e disparam re-renderizações da tela.
5.  **Efeitos Colaterais com `useEffect`:** Como reagir a mudanças de estado ou consultar dados ao carregar a página (consumo de APIs em React).
6.  **Gerenciamento de Ferramentas:** Aprenda a inicializar um projeto moderno usando o **Vite** no lugar do antigo CRA (Create React App).

### Materiais Recomendados (React):
*   **[Documentação Oficial - React.dev (Em Português)](https://pt-br.react.dev/):** Comece pelo guia de "Início Rápido". É, sem dúvidas, a melhor fonte atual. Ensina o padrão moderno (Functional Components e Hooks).
*   **[Rocketseat (Discover e Ignite)](https://www.rocketseat.com.br/):** Possuem trilhas gratuitas iniciais focadas fortemente no ecossistema e ferramentas modernas de React.
*   **Projetos Práticos (YouTube):** Busque por "Construindo [App] com React Vite" (ex: ToDo List, App de Clima) para ver a teoria sendo aplicada.

---

## Módulo 4: Ferramentas do Dia a Dia e Boas Práticas

Para atuar no mercado, codar não é suficiente. É preciso saber como um dev trabalha na prática.

1.  **VS Code (Editor de Código):** O editor padrão da indústria. Integre ferramentas como o *Prettier* (para formatar seu código) e *ESLint* (para encontrar erros rapidamente).
2.  **Git e GitHub (Controle de Versão):** Vital para trabalho em equipe e seu portfólio. Aprenda o básico: `git clone`, `git add`, `git commit`, `git push`, criação de `branches` e abertura de Pull Requests (PRs).
3.  **Frontend Mentor:** Quando passar da fase de tutoriais em vídeo, acesse o [Frontend Mentor](https://www.frontendmentor.io/). A plataforma te dá desafios reais (um design no Figma/Imagem) para você transformar em código (HTML/CSS/JS e React).

## Roteiro Final de Estudos Sugerido para o Aluno ADS:

1.  **Semanas 1-2:** Fundamentos de HTML e CSS. Construa páginas simples não responsivas.
2.  **Semanas 3-4:** Flexbox, CSS Grid e media queries para sites em celular (Mobile First).
3.  **Semanas 5-8:** JavaScript Puro (Lógica pesada, manipulação da tela, consumo de sua primeira API via fetch).
4.  **Semanas 9-12:** React (Componentes Funcionais, useState e useEffect).
5.  **Projetos Constantes:** Jamais veja a teoria sem criar uma aplicação relacionada a ela em seguida (Ex: aprendeu Arrays e Loops? Faça uma lista de tarefas. Aprendeu Fetch API? Faça um buscador de pokémons ou filmes).
