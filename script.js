// Configuração GSAP e Plugins
gsap.registerPlugin(ScrollTrigger);

// 1. Cursor Follower Otimizado (QuickTo)
const cursor = document.querySelector(".cursor");
const xTo = gsap.quickTo(cursor, "x", {duration: 0.2, ease: "power3"});
const yTo = gsap.quickTo(cursor, "y", {duration: 0.2, ease: "power3"});

window.addEventListener("mousemove", (e) => {
    xTo(e.clientX);
    yTo(e.clientY);
});

// Magnetic Links Effect
const interactives = document.querySelectorAll("a, button, .card-pain");
interactives.forEach(el => {
    el.addEventListener("mouseenter", () => {
        gsap.to(cursor, { scale: 3, backgroundColor: "rgba(255,255,255,1)", duration: 0.3 });
    });
    el.addEventListener("mouseleave", () => {
        gsap.to(cursor, { scale: 1, backgroundColor: "#00F0FF", duration: 0.3 });
    });
});

// 2. Animação de Entrada: Hero Section 
const splitHeadline = new SplitType('.headline', { types: 'words, chars' });

const tl = gsap.timeline();

// Header Slide Down
tl.from(".header", {
    duration: 1.2,
    y: -50,
    opacity: 0,
    ease: "power3.out",
    delay: 0.2
})
// Pill Badge Drop
.from(".pill-badge", {
    duration: 0.6,
    y: 20,
    opacity: 0,
    ease: "back.out(1.5)"
}, "-=0.8")
// Headline Characters Matrix Rise
.from(splitHeadline.chars, {
    duration: 1.2,
    y: 100, 
    rotationZ: 15,
    opacity: 0,
    stagger: 0.03,
    ease: "back.out(2)" 
}, "-=0.6")
// Subheadline & CTA Fade In Up
.from(".subheadline, .cta-container, .trust-indicators", {
    duration: 1,
    y: 30,
    opacity: 0,
    stagger: 0.15,
    ease: "power3.out"
}, "-=0.8");

// 3. Efeito Parallax nos Elementos 3D Glassmorphism
const heroVisual = document.querySelector(".hero-visual");

gsap.from(".g-1", { duration: 1.5, x: -100, opacity: 0, rotationY: 45, ease: "back.out(1.2)", delay: 1 });
gsap.from(".g-2", { duration: 1.5, x: 100, opacity: 0, rotationY: -45, ease: "back.out(1.2)", delay: 1.2 });

document.addEventListener("mousemove", (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 2;
    const y = (e.clientY / window.innerHeight - 0.5) * 2;
    
    // Movimento suave OPOSTO ao mouse (Efeito de Câmera 3D)
    gsap.to(".g-1", { x: x * 40, y: y * 40, rotationY: x * 20 - 15, rotationX: y * -20 + 10, duration: 1.5, ease: "power2.out" });
    gsap.to(".g-2", { x: x * -50, y: y * -50, rotationY: x * -20 + 15, rotationX: y * 20 - 5, duration: 1.5, ease: "power2.out" });
});

// 4. Seção "Pain Points" ativada pelo Scroll
const splitTitle = new SplitType('.section-title', { types: 'words' });

gsap.from(splitTitle.words, {
    scrollTrigger: {
        trigger: ".pain-points-section",
        start: "top 75%",
    },
    duration: 1,
    y: 50,
    opacity: 0,
    stagger: 0.1,
    ease: "power3.out"
});

gsap.from(".section-subtitle", {
    scrollTrigger: {
        trigger: ".pain-points-section",
        start: "top 70%",
    },
    duration: 1,
    y: 30,
    opacity: 0,
    ease: "power3.out",
    delay: 0.3
});

// Stagger (Explosão Direcional) nos Cards
gsap.to(".card-pain", {
    scrollTrigger: {
        trigger: ".cards-container",
        start: "top 80%",
    },
    duration: 1,
    y: 0,
    opacity: 1,
    stagger: 0.2, // Um surge após o outro
    ease: "back.out(1.5)"
});

// 5. Final CTA Reveal
gsap.from(".cta-box", {
    scrollTrigger: {
        trigger: ".final-cta",
        start: "top 70%",
    },
    duration: 1.5,
    scale: 0.8,
    opacity: 0,
    rotationX: 20,
    ease: "back.out(1.2)"
});
