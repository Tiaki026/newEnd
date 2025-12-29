// static/js/script.js
// Общие скрипты для всего сайта
document.addEventListener('DOMContentLoaded', function() {
    // Автоматическое скрытие алертов через 5 секунд
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Подтверждение удаления
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить этого персонажа?')) {
                e.preventDefault();
            }
        });
    });
});