const currentLocation = window.location.href;
console.log("window.location.href ->", currentLocation);
const navLinks = document.querySelectorAll('nav ul li a');

navLinks.forEach(link => {
    console.log("link.href ->", link.href);
    if (link.href == currentLocation) {
        link.classList.add('active');
    }
});