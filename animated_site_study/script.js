// Registrar plugins do GSAP
gsap.registerPlugin(ScrollTrigger);

// ------------------------------------------------------------------
// 1. Mouse Customizado Magnético (Cursor Follower)
// ------------------------------------------------------------------
const cursor = document.querySelector(".cursor");
let mouseX = window.innerWidth / 2;
let mouseY = window.innerHeight / 2;

// Rastrear mouse suavemente via GSAP QuickTo para ultra-performance (60+ FPS)
const xTo = gsap.quickTo(cursor, "x", {duration: 0.2, ease: "power3"});
const yTo = gsap.quickTo(cursor, "y", {duration: 0.2, ease: "power3"});

window.addEventListener("mousemove", (e) => {
    xTo(e.clientX);
    yTo(e.clientY);
    mouseX = e.clientX;
    mouseY = e.clientY;
});

// Cursor "inchando" (Magnetic Effect) ao passar em interativos
const interactives = document.querySelectorAll("a, button, .grid-item");
interactives.forEach(el => {
    el.addEventListener("mouseenter", () => {
        gsap.to(cursor, { scale: 3, backgroundColor: "rgba(255,255,255,1)", duration: 0.3 });
    });
    el.addEventListener("mouseleave", () => {
        gsap.to(cursor, { scale: 1, backgroundColor: "#00d2ff", duration: 0.3 });
    });
});

// ------------------------------------------------------------------
// 2. Text Reveal (Surgindo Palavra por Palavra)
// ------------------------------------------------------------------
// O SplitType "fatia" nosso HTML em palavras limpas para animarmos independentes
const splitHeadline = new SplitType('.headline', { types: 'words, chars' });

const tl = gsap.timeline();

tl.from(".header", {
    duration: 1.2,
    y: -50,
    opacity: 0,
    ease: "power3.out",
    delay: 0.2
})
// Animação das Letrinhas vindo de baixo pra cima, estilo Matrix 
.from(splitHeadline.chars, {
    duration: 1,
    y: 100, // Vem de 100px abaixo
    rotationZ: 10,
    opacity: 0,
    stagger: 0.05, // Intervalo cascata de 0.05s por letra!
    ease: "back.out(2)" // "Estilingue" com um pouco de exagero
}, "-=0.8")
.from(".subheadline, .cta-container", {
    duration: 0.8,
    y: 30,
    opacity: 0,
    stagger: 0.2,
    ease: "power3.out"
}, "-=0.5");

// ------------------------------------------------------------------
// 3. Efeito Parallax Direcional (Hero Section)
// ------------------------------------------------------------------
const heroSection = document.querySelector(".hero-section");
heroSection.addEventListener("mousemove", (e) => {
    // Calcula posição de -1 a 1 baseado no centro do monitor
    const x = (e.clientX / window.innerWidth - 0.5) * 2;
    const y = (e.clientY / window.innerHeight - 0.5) * 2;
    
    // As formas flutuam na direção OPOSTA (-x, -y) à rolagem do mouse!
    gsap.to(".circle", { x: x * 60, y: y * 60, duration: 1, ease: "power2.out" });
    gsap.to(".square", { x: x * -40, y: y * -40, rotation: "+=1", duration: 1, ease: "power2.out" });
    gsap.to(".triangle", { x: x * 30, y: y * -30, rotation: "-=1", duration: 1, ease: "power2.out" });
});

// Quando ninguém mexe no mouse, manter animação orgânica:
gsap.to(".circle", { y: "+=20", duration: 2, yoyo: true, repeat: -1, ease: "sine.inOut" });
gsap.to(".square", { y: "-=15", rotation: "+=15", duration: 3, yoyo: true, repeat: -1, ease: "sine.inOut" });
gsap.to(".triangle", { y: "+=10", rotation: "-=10", duration: 2.5, yoyo: true, repeat: -1, ease: "sine.inOut" });


// ------------------------------------------------------------------
// 4. Mágica do Scroll (ScrollTrigger Avançado)
// ------------------------------------------------------------------
gsap.from(".scroll-title", {
    scrollTrigger: {
        trigger: ".scroll-section",
        start: "top 75%",
    },
    duration: 1.2,
    y: 100,
    opacity: 0,
    ease: "back.out(1.5)"
});

// Cards acompanhando
gsap.to(".card", {
    scrollTrigger: {
        trigger: ".cards-container",
        start: "top 80%",
    },
    duration: 1,
    y: 0,
    opacity: 1,
    stagger: 0.2,
    ease: "power3.out"
});

// ------------------------------------------------------------------
// 5. O Grid "Explosivo" (Stagger From Center)
// ------------------------------------------------------------------
gsap.to(".grid-item", {
    scrollTrigger: {
        trigger: ".grid-section",
        start: "top 60%", // Aciona quando a div atinge 60% da página
    },
    scale: 1,
    opacity: 1,
    ease: "back.out(2)",
    stagger: {
        grid: [2, 3], // Dizemos ao GSAP qual a forma visível da nossa grid do HTML para ele calcular a distância radial
        from: "center", // Começa a surgir partindo do card do meio (explode pra fora)
        amount: 0.8     // Demora 0.8s pra concluir a onda toda
    }
});
