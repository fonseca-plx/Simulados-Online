document.addEventListener('DOMContentLoaded', function () {
    const rows = document.querySelectorAll('.clickable-row');

    rows.forEach(function (row) {
        row.addEventListener('click', function () {
            const href = this.getAttribute('data-href');
            if (href) {
                window.location.href = href;
            }
        });

        // Adiciona efeito visual ao passar o mouse
        row.addEventListener('mouseenter', function () {
            this.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
        });

        row.addEventListener('mouseleave', function () {
            this.style.boxShadow = 'none';
        });
    });
});