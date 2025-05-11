document.addEventListener('DOMContentLoaded', function () {
    let themeButton = document.getElementById("theme-button");
    const toggleDarkMode = () => {
      var element = document.body;
      element.classList.toggle("dark-mode");
    }
    themeButton.addEventListener("click", toggleDarkMode);})