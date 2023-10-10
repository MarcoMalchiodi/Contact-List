const selectOption = document.getElementById('selectOption');
const search = document.getElementById('search');
// Add an event listener to the select element
selectOption.addEventListener('change', function () {
    // Automatically submit the form when a selection is made
    search.submit();
});