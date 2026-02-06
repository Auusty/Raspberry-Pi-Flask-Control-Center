function updateHeaderTime() {
    const el = document.getElementById("header-time");
    if (!el) return;

    const now = new Date();
    el.textContent = now.toLocaleTimeString([], {
        hour: "numeric",
        minute: "2-digit"
    });
}

updateHeaderTime();
setInterval(updateHeaderTime, 1000);
