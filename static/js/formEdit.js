function enableEdit(field) {
    const label = document.querySelector(`label[for=${field}]`);
    const input = document.getElementById(field);

    // Hide the text and show the input
    label.style.display = "none";
    input.style.display = "inline-block";

    // Focus the input to allow immediate editing
    input.focus();
}

function disableEdit(field) {
    const label = document.querySelector(`label[for=${field}]`);
    const input = document.getElementById(field);

    // Hide the input and show the text again
    label.style.display = "inline-block";
    input.style.display = "none";

    // Update the text with the new value from the input
    label.innerText = input.value;
}

document.querySelectorAll('.editable-input').forEach(input => {
    const label = input.previousElementSibling;

    if (label && input.readOnly) {
        label.style.cursor = 'default';
    }
});