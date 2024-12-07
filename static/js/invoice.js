document.addEventListener("DOMContentLoaded", function () {
    const serviceSelect = document.getElementById("service-select");
    const quantityInput = document.getElementById("quantity-input");
    const addServiceButton = document.getElementById("add-service");
    const selectedServicesTable = document.getElementById("selected-services").querySelector("tbody");
    const totalAmountSpan = document.getElementById("total-amount");

    let totalCost = 0;
    let totalRows = 0;

    function updateTotalCost() {
        const rows = selectedServicesTable.querySelectorAll("tr");
        totalCost = 0;
        rows.forEach(row => {
            const totalCell = row.querySelector(".service-total");
            totalCost += parseFloat(totalCell.textContent);
        });
        totalAmountSpan.textContent = totalCost.toFixed(2);
    }

    function isServiceAlreadyAdded(serviceName) {
        const rows = selectedServicesTable.querySelectorAll("tr");
        for (const row of rows) {
            const rowServiceName = row.cells[0].textContent;
            if (rowServiceName === serviceName) {
                return true;
            }
        }
        return false;
    }

    function addService() {
        const selectedOption = serviceSelect.options[serviceSelect.selectedIndex];
        const serviceId = selectedOption.value;
        const serviceName = selectedOption.text;
        const servicePrice = parseFloat(selectedOption.getAttribute("data-price"));
        const quantity = parseInt(quantityInput.value);

        if (quantity <= 0 || quantity > 3) return;
        if (totalRows >= 3) return;
        if (isServiceAlreadyAdded(serviceName)) return;

        const serviceTotal = (servicePrice * quantity).toFixed(2);

        // Add new row to the table
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${serviceName}</td>
            <td>${quantity}</td>
            <td>$${servicePrice.toFixed(2)}</td>
            <td class="service-total">${serviceTotal}</td>
            <td><button class="remove-service">Remove</button></td>
        `;
        selectedServicesTable.appendChild(row);

        totalRows += 1;
        updateTotalCost();

        // Add event listener for remove button
        row.querySelector(".remove-service").addEventListener("click", function () {
            row.remove();
            totalRows -= 1;
            updateTotalCost();
        });
    }

    // Add event listener to Add Service button
    addServiceButton.addEventListener("click", addService);
});