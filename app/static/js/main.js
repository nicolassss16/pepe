// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {

    /* --- Toggle de Tema (Modo Oscuro/Claro) --- */
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        // Carga la preferencia guardada
        const currentTheme = localStorage.getItem('theme');
        if (currentTheme === 'dark') {
            document.body.classList.add('dark-mode');
            themeToggle.innerHTML = '<i class="fas fa-sun" aria-hidden="true"></i>';
        }

        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            
            // Guarda la preferencia
            let theme = 'light';
            if (document.body.classList.contains('dark-mode')) {
                theme = 'dark';
                themeToggle.innerHTML = '<i class="fas fa-sun" aria-hidden="true"></i>';
            } else {
                themeToggle.innerHTML = '<i class="fas fa-moon" aria-hidden="true"></i>';
            }
            localStorage.setItem('theme', theme);
        });
    }

    /* --- Dropdown de Menú de Usuario --- */
    const userMenu = document.querySelector('.user-menu');
    if (userMenu) {
        const userButton = userMenu.querySelector('.user-button');
        const userDropdown = userMenu.querySelector('.user-dropdown');

        userButton.addEventListener('click', (e) => {
            e.stopPropagation(); // Evita que el clic se propague al 'document'
            const isHidden = userDropdown.hasAttribute('hidden');
            if (isHidden) {
                userDropdown.removeAttribute('hidden');
                userButton.setAttribute('aria-expanded', 'true');
            } else {
                userDropdown.setAttribute('hidden', '');
                userButton.setAttribute('aria-expanded', 'false');
            }
        });

        // Cierra el dropdown si se hace clic fuera
        document.addEventListener('click', (e) => {
            if (!userMenu.contains(e.target)) {
                userDropdown.setAttribute('hidden', '');
                userButton.setAttribute('aria-expanded', 'false');
            }
        });
    }

    /* --- Menú Móvil --- */
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (mobileMenuToggle && navLinks) {
        mobileMenuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
            const isExpanded = navLinks.classList.contains('open');
            mobileMenuToggle.setAttribute('aria-expanded', isExpanded);
        });
    }

    /* --- Cerrar Alertas --- */
    const alertClosers = document.querySelectorAll('.alert-close');
    alertClosers.forEach(button => {
        button.addEventListener('click', (e) => {
            const alert = e.target.closest('.alert');
            if (alert) {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 300); // Remueve después de la transición
            }
        });
    });

    /* --- Lógica del Formulario de Compra --- */
    const purchaseForm = document.getElementById('purchase-form');
    if (purchaseForm) {
        const eventSelect = document.getElementById('event');
        const quantityInput = document.getElementById('quantity');
        const quantityPlus = purchaseForm.querySelector('.quantity-btn.plus');
        const quantityMinus = purchaseForm.querySelector('.quantity-btn.minus');
        const unitPriceSpan = purchaseForm.querySelector('.unit-price');
        const totalPriceSpan = purchaseForm.querySelector('.total-price');
        const availableTicketsSpan = document.querySelector('.available-tickets');

        // Función para actualizar el precio
        function updatePrice() {
            const selectedOption = eventSelect.options[eventSelect.selectedIndex];
            const price = parseFloat(selectedOption.dataset.price) || 0;
            const quantity = parseInt(quantityInput.value) || 0;
            const total = price * quantity;

            unitPriceSpan.textContent = `$${price.toFixed(2)}`;
            totalPriceSpan.textContent = `$${total.toFixed(2)}`;
            
            // Actualiza tickets disponibles
            if(selectedOption.value) {
                const available = selectedOption.dataset.available || 'N/A';
                availableTicketsSpan.textContent = `(${available} disponibles)`;
                // Ajusta el max del input de cantidad
                quantityInput.max = available;
            } else {
                availableTicketsSpan.textContent = '';
            }
        }

        // Botones de cantidad
        quantityPlus.addEventListener('click', () => {
            const max = parseInt(quantityInput.max) || 10;
            if (quantityInput.value < max) {
                quantityInput.value = parseInt(quantityInput.value) + 1;
                updatePrice(); // Llama a la actualización
            }
        });

        quantityMinus.addEventListener('click', () => {
            if (quantityInput.value > 1) {
                quantityInput.value = parseInt(quantityInput.value) - 1;
                updatePrice(); // Llama a la actualización
            }
        });

        // Event Listeners
        eventSelect.addEventListener('change', updatePrice);
        quantityInput.addEventListener('input', updatePrice);

        // Inicializa el precio al cargar
        updatePrice();
    }
    
    /* --- Scroll Suave para "Comprar" --- */
    const scrollLinks = document.querySelectorAll('.scroll-to-buy');
    const purchaseSection = document.getElementById('comprar');
    
    if (purchaseSection && scrollLinks.length > 0) {
        scrollLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                purchaseSection.scrollIntoView({ behavior: 'smooth' });
            });
        });
    }
});
