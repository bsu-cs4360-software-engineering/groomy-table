document.addEventListener("DOMContentLoaded", function() {
    const footer = document.querySelector('footer');
    const main = document.querySelector('main');

    function adjustMainMargin() {
        const footerHeight = footer.offsetHeight;
        main.style.marginBottom = `${footerHeight}px`;
    }

    adjustMainMargin();
    window.addEventListener('resize', adjustMainMargin);
});