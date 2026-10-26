const yearElement = document.getElementById("current-year");

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

document.querySelectorAll("[data-days-left]").forEach((element) => {
    const days = Number(element.dataset.daysLeft);
    if (days >= 0 && days <= 30) {
        element.classList.add("text-danger", "fw-bold");
        element.title = "Фестиваль меньше чем через месяц";
    }
});
