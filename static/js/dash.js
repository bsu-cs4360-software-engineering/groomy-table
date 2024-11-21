function deleteItem(promptMessage, serviceId) {
    if (confirm(promptMessage)) {
        // Submit the form corresponding to the clicked service
        document.getElementById('delete-form-' + serviceId).submit();
    }
    return false; // Prevent default anchor behavior
}