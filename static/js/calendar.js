document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".calendar-container");
    const year = container.querySelector(".year");
    const triangleLeft = container.querySelector(".triangle-left");
    const triangleRight = container.querySelector(".triangle-right");
    const months = container.querySelectorAll(".month");
    const days = container.querySelector(".num-dates");
    const dateDisplay = container.querySelector(".calendar-left");

    let today = new Date();
    // Set time to midnight
    today.setHours(0, 0, 0, 0);
    let currentYear = today.getFullYear();
    let selectedYear = currentYear;
    let selectedMonth = today.getMonth();
    let selectedDay = null;
    
    const dayLimitStart = new Date(today);
    const dayLimitEnd = new Date(today);
    dayLimitStart.setDate(today.getDate() + 1); // Tomorrow, 00:00
    dayLimitEnd.setMonth(today.getMonth() + 1); // One month from tomorrow, 00:00

    // Initialize calendar with current year
    year.textContent = currentYear;

    function updateYear(direction) {
        if (direction == "left" && selectedYear > currentYear) {
            selectedYear--;
        } else if (direction == "right") {
            selectedYear++;
        }

        year.textContent = selectedYear;
        updateMonth();
        // Re-render if a month is already selected
        if (selectedMonth !== null) renderDays(selectedMonth);
    }

    // Year navigation
    triangleLeft.addEventListener("click", () => updateYear("left"));
    triangleRight.addEventListener("click", () => updateYear("right"));

    // Month selection
    months.forEach((month, index) => {
        month.addEventListener("click", () => {
            // Restrict selection before current month
            if (selectedYear === currentYear && index < today.getMonth()) return;
            // Clear active class from all months
            months.forEach(m => m.classList.remove("active"));
            // Set active class on selected month
            month.classList.add("active");
            selectedMonth = index;
            renderDays(selectedMonth);
        });
    });

    // Render days in the month
    function renderDays(monthIndex) {
        // Clear existing days
        days.innerHTML = "";
        const firstDayOfMonth = new Date(selectedYear, monthIndex, 1).getDay()
        const daysInMonth = new Date(selectedYear, monthIndex + 1, 0).getDate()
        let day = 1 - firstDayOfMonth;

        // Generate weeks of the month
        while (day <= daysInMonth) {
            const weekRow = document.createElement("div");
            weekRow.classList.add("week");
            for (let i = 0; i < 7; i++, day++) {
                const dayElement = document.createElement("span");
                dayElement.classList.add("day");
                if (day < 1 || day > daysInMonth) {
                    dayElement.textContent = "";
                } else {
                    const date = new Date(selectedYear, monthIndex, day);
                    date.setHours(0, 0, 0, 0); // Clear time for comparison
                    dayElement.textContent = String(day).padStart(2, '0'); // Format as two digits
                    // Restrict selection to within tomorrow and one month from tomorrow
                    if (date >= dayLimitStart && date <= dayLimitEnd) {
                        dayElement.classList.add("selectable");
                        dayElement.addEventListener("click", () => selectDay(dayElement, date));

                        // Set tomorrow as the default selected day
                        if (date.getTime() === dayLimitStart.getTime()) {
                            dayElement.classList.add("active");
                            selectDay(dayElement, date);
                        }
                    } else {
                        dayElement.classList.add("inactive");
                    }
                }

                weekRow.appendChild(dayElement);
            }

            days.appendChild(weekRow);
        }
    }

    // Handle day selection
    function selectDay(dayElement, date) {
        // Clear previous selection
        days.querySelectorAll(".active").forEach(el => el.classList.remove("active"));
        dayElement.classList.add("active");
        selectedDay = String(date.getDate()).padStart(2, '0'); // Format as two digits

        dateDisplay.querySelector(".num-date").textContent = selectedDay;
        dateDisplay.querySelector(".num-date-day").textContent = date.toLocaleDateString("en-US", { weekday: "long" });
    }

    function updateMonth() {
        months.forEach((month, index) => {
            month.classList.toggle("inactive", selectedYear === currentYear && index < today.getMonth());
        });
    }

    // Initialize months to show which are inactive
    updateMonth();
    // Set current month as active
    months[selectedMonth].classList.add("active");
    // Render days for current month
    renderDays(selectedMonth);
});