document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("menuBtn");
  const nav = document.getElementById("nav");
  if (btn && nav) btn.addEventListener("click", () => nav.classList.toggle("open"));

  nav?.querySelectorAll("a[href^='#']").forEach(a=>{
    a.addEventListener("click", e=>{
      e.preventDefault();
      const id = a.getAttribute("href");
      const el = document.querySelector(id);
      if (!el) return;
      const y = el.getBoundingClientRect().top + window.scrollY - 64;
      window.scrollTo({top:y, behavior:"smooth"});
      nav.classList.remove("open");
    });
  });

  const y = document.getElementById("y");
  if (y) y.textContent = new Date().getFullYear();
});
