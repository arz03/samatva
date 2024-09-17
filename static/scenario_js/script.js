document.addEventListener("DOMContentLoaded", function() {
    const optionButtons = document.querySelectorAll('.option-btn');

    optionButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.closest('form').submit();
        });
    });
});
