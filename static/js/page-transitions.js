(() => {
    const DURATION = 140; // must match CSS fade-out

    function navigate(href) {
        const page = document.querySelector(".page");
        if (!page) {
            window.location.href = href;
            return;
        }

        page.classList.add("exiting");

        setTimeout(() => {
            window.location.href = href;
        }, DURATION);
    }

    // Intercept normal links
    document.addEventListener("click", e => {
        const link = e.target.closest("a[href]");
        if (!link) return;

        // Allow external links / new tabs if you ever add them
        if (link.target === "_blank") return;

        e.preventDefault();
        navigate(link.href);
    });

    // Expose helper for buttons
    window.navigateTo = navigate;
})();
