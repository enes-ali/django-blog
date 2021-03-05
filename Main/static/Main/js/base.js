const openSearch = document.getElementById("open-search");
const closeSearch = document.getElementById("close-search");
const searchOverlay = document.getElementById("search-overlay");
const scrollToTop = document.querySelector(".scroll-top");

// Open and Close Search layout
openSearch.addEventListener("click", (event) => {
    searchOverlay.style.visibility = "visible";
    searchOverlay.style.opacity = "100%";
    document.documentElement.classList.add("no-scroll");
});

closeSearch.addEventListener("click", (event) => {
    searchOverlay.style.opacity = "0%";
    setTimeout(() => searchOverlay.style.visibility = "hidden", 500);
    document.documentElement.classList.remove("no-scroll");
});


// Show Scroll To Top
window.addEventListener("scroll", (event) => {
    if(window.pageYOffset > 600)
        scrollToTop.classList.add("scroll-top-active");
    
    else
        scrollToTop.classList.remove("scroll-top-active");
});

// Scroll To Top
scrollToTop.addEventListener("click", (event) => {
    window.scrollTo({left: 0, top: 0, behavior:"smooth", });
});