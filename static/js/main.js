/**
 * Главный JavaScript файл для лендинга "Здоровый Пар"
 */

// Плавная прокрутка к секции
function scrollToSection(id) {
    const element = document.getElementById(id);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
        // Закрываем мобильное меню если открыто
        closeMobileMenu();
    }
}

// Мобильное меню
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    const closeIcon = document.getElementById('close-icon');
    
    if (menu && menuIcon && closeIcon) {
        const isHidden = menu.classList.contains('hidden');
        
        if (isHidden) {
            menu.classList.remove('hidden');
            menuIcon.classList.add('hidden');
            closeIcon.classList.remove('hidden');
        } else {
            menu.classList.add('hidden');
            menuIcon.classList.remove('hidden');
            closeIcon.classList.add('hidden');
        }
    }
}

function closeMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    const closeIcon = document.getElementById('close-icon');
    
    if (menu && menuIcon && closeIcon) {
        menu.classList.add('hidden');
        menuIcon.classList.remove('hidden');
        closeIcon.classList.add('hidden');
    }
}

// Модальное окно заказа
function openOrderForm() {
    const modal = document.getElementById('order-modal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        document.body.style.overflow = 'hidden'; // Блокируем скролл страницы
    }
}

function closeOrderForm() {
    const modal = document.getElementById('order-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        document.body.style.overflow = ''; // Разблокируем скролл
        // Сбрасываем форму
        resetOrderForm();
    }
}

function resetOrderForm() {
    const form = document.getElementById('order-form');
    const successMessage = document.getElementById('success-message');
    
    if (form) {
        form.reset();
        form.classList.remove('hidden');
    }
    
    if (successMessage) {
        successMessage.classList.add('hidden');
    }
}

// Обработка отправки формы заказа
async function handleOrderSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const data = {
        name: formData.get('name'),
        phone: formData.get('phone'),
        product: formData.get('product'),
        quantity: formData.get('quantity'),
        comment: formData.get('comment') || ''
    };
    
    // Валидация
    if (!data.name || !data.phone || !data.product || !data.quantity) {
        alert('Пожалуйста, заполните все обязательные поля');
        return;
    }
    
    try {
        const response = await fetch('/api/order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Показываем сообщение об успехе
            const formElement = document.getElementById('order-form');
            const successMessage = document.getElementById('success-message');
            
            if (formElement) {
                formElement.classList.add('hidden');
            }
            
            if (successMessage) {
                successMessage.classList.remove('hidden');
            }
            
            // Закрываем модальное окно через 3 секунды
            setTimeout(() => {
                closeOrderForm();
            }, 3000);
        } else {
            alert(result.error || 'Произошла ошибка при отправке заявки');
        }
    } catch (error) {
        console.error('Ошибка при отправке заказа:', error);
        alert('Произошла ошибка при отправке заявки. Попробуйте позже.');
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    // Мобильное меню
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', toggleMobileMenu);
    }
    
    // Закрытие модального окна по клику вне его
    const modal = document.getElementById('order-modal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeOrderForm();
            }
        });
    }
    
    // Закрытие модального окна по Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeOrderForm();
        }
    });
    
    // Обработка формы заказа
    const orderForm = document.getElementById('order-form');
    if (orderForm) {
        orderForm.addEventListener('submit', handleOrderSubmit);
    }
    
    // Закрытие мобильного меню при клике на ссылку
    const mobileMenuLinks = document.querySelectorAll('#mobile-menu button');
    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });
});

// Экспортируем функции для глобального использования
window.scrollToSection = scrollToSection;
window.openOrderForm = openOrderForm;
window.closeOrderForm = closeOrderForm;

