// static/js/main.js

// Loader
window.addEventListener('load', () => {
    const loader = document.getElementById('loader');
    loader.classList.add('hidden');
});

// Dark Mode Toggle
document.getElementById('theme-switch').addEventListener('change', () => {
    document.body.classList.toggle('dark-mode');
});

// Google Maps for Contact Page
function initMap() {
    if (document.getElementById('map')) {
        const location = { lat: 4.6749, lng: -75.7817 }; // Coordenadas de Alcalá, Valle del Cauca
        const map = new google.maps.Map(document.getElementById('map'), {
            zoom: 15,
            center: location
        });
        new google.maps.Marker({
            position: location,
            map: map,
            title: 'El Galpón'
        });
    }
}

// Carrito
let cart = JSON.parse(localStorage.getItem('cart')) || [];
updateCartCount();

function updateCartCount() {
    const cartCount = document.getElementById('cart-count');
    if (cartCount) {
        cartCount.textContent = cart.length;
    }
}

function addToCart(productId) {
    cart.push(productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    showToast('Producto añadido al carrito', 'success');
}

// Carrito - Mostrar productos
function displayCart() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    if (!cartItems || !cartTotal) return;

    cartItems.innerHTML = '';
    let total = 0;

    const productPromises = cart.map(productId => {
        return fetch(`/api/products/${productId}/`)
            .then(response => response.json())
            .catch(() => null);
    });

    Promise.all(productPromises).then(products => {
        products.forEach(product => {
            if (product) {
                const item = document.createElement('div');
                item.className = 'product';
                item.innerHTML = `
                    <img src="${product.imagen || '/static/images/placeholder.jpg'}" alt="${product.nombre}">
                    <h4>${product.nombre}</h4>
                    <p>Precio: $${product.precio}</p>
                `;
                cartItems.appendChild(item);
                total += parseFloat(product.precio);
            }
        });

        cartTotal.textContent = `Total: $${total.toFixed(2)}`;
    });
}

// Vaciar Carrito
document.getElementById('clear-cart')?.addEventListener('click', () => {
    cart = [];
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    displayCart();
    showToast('Carrito vaciado', 'success');
});

// Carrusel
let currentSlide = 0;
const slides = document.querySelectorAll('.carousel-slide');
const totalSlides = slides.length;

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.style.transform = `translateX(${(i - index) * 100}%)`;
    });
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(currentSlide);
}

document.getElementById('next-slide')?.addEventListener('click', nextSlide);
document.getElementById('prev-slide')?.addEventListener('click', prevSlide);

// Auto-slide
if (totalSlides > 0) {
    showSlide(currentSlide);
    setInterval(nextSlide, 5000);
}

// Favoritos
let favorites = JSON.parse(localStorage.getItem('favorites')) || [];

function toggleFavorite(productId) {
    const button = document.getElementById(`favorite-${productId}`);
    if (favorites.includes(productId)) {
        favorites = favorites.filter(id => id !== productId);
        button.classList.remove('favorited');
        showToast('Eliminado de favoritos', 'error');
    } else {
        favorites.push(productId);
        button.classList.add('favorited');
        showToast('Añadido a favoritos', 'success');
    }
    localStorage.setItem('favorites', JSON.stringify(favorites));
}

// Compartir Producto
function shareProduct(name, url) {
    if (navigator.share) {
        navigator.share({
            title: `Mira este producto: ${name}`,
            url: url
        }).catch(err => console.error('Error al compartir:', err));
    } else {
        navigator.clipboard.writeText(url).then(() => {
            showToast('Enlace copiado al portapapeles', 'success');
        });
    }
}

// Vista Rápida
function openQuickView(productId) {
    fetch(`/api/products/${productId}/`)
        .then(response => response.json())
        .then(product => {
            const modal = document.getElementById('quick-view-modal');
            const content = document.getElementById('quick-view-content');
            content.innerHTML = `
                <img src="${product.imagen || '/static/images/placeholder.jpg'}" alt="${product.nombre}">
                <h3>${product.nombre}</h3>
                <p>${product.descripcion}</p>
                <p>Categoría: ${product.categoria}</p>
                <p>Especie: ${product.especie}</p>
                <p>Precio: $${product.precio}</p>
                <p>Stock: ${product.stock}</p>
                <button onclick="addToCart(${product.id})">Añadir al Carrito</button>
            `;
            modal.style.display = 'flex';
        })
        .catch(err => {
            console.error('Error al cargar el producto:', err);
            showToast('Error al cargar el producto', 'error');
        });
}

function closeQuickView() {
    const modal = document.getElementById('quick-view-modal');
    modal.style.display = 'none';
}

// Reseñas
let reviews = JSON.parse(localStorage.getItem('reviews')) || {};

function displayReviews(productId) {
    const reviewContainer = document.getElementById(`reviews-${productId}`);
    if (!reviewContainer) return;

    reviewContainer.innerHTML = '';
    const productReviews = reviews[productId] || [];
    productReviews.forEach(review => {
        const reviewElement = document.createElement('div');
        reviewElement.className = 'review';
        reviewElement.innerHTML = `
            <p>Calificación: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
            <p>${review.comment}</p>
        `;
        reviewContainer.appendChild(reviewElement);
    });
}

function submitReview(productId) {
    const rating = document.getElementById(`rating-${productId}`).value;
    const comment = document.getElementById(`comment-${productId}`).value.trim();

    if (!rating || !comment) {
        showToast('Por favor, completa la calificación y el comentario', 'error');
        return;
    }

    if (!reviews[productId]) reviews[productId] = [];
    reviews[productId].push({ rating: parseInt(rating), comment });
    localStorage.setItem('reviews', JSON.stringify(reviews));
    displayReviews(productId);
    showToast('Reseña enviada', 'success');

    document.getElementById(`rating-${productId}`).value = '';
    document.getElementById(`comment-${productId}`).value = '';
}

// Filtros y Búsqueda
function applyFilters() {
    const searchInput = document.getElementById('search-input')?.value.toLowerCase() || '';
    const categoriaFilter = document.getElementById('categoria-filter')?.value;
    const especieFilter = document.getElementById('especie-filter')?.value;
    const sortFilter = document.getElementById('sort-filter')?.value;

    const url = new URL(window.location);
    url.searchParams.set('search', searchInput);
    url.searchParams.set('categoria', categoriaFilter || '');
    url.searchParams.set('especie', especieFilter || '');
    url.searchParams.set('sort', sortFilter || '');
    window.location = url;
}

document.getElementById('search-input')?.addEventListener('input', applyFilters);
document.getElementById('categoria-filter')?.addEventListener('change', applyFilters);
document.getElementById('especie-filter')?.addEventListener('change', applyFilters);
document.getElementById('sort-filter')?.addEventListener('change', applyFilters);

// Toast Notifications
function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.getElementById('toast-container').appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// static/js/main.js
// Funciones para el modal de autenticación
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Cerrar el modal al hacer clic fuera de él
window.onclick = function(event) {
    const loginModal = document.getElementById('login-modal');
    const registerModal = document.getElementById('register-modal');
    if (event.target === loginModal) {
        loginModal.style.display = 'none';
    }
    if (event.target === registerModal) {
        registerModal.style.display = 'none';
    }
};

// Funciones para el chatbot
function toggleChatbot() {
    const chatbotWindow = document.getElementById('chatbot-window');
    chatbotWindow.style.display = chatbotWindow.style.display === 'block' ? 'none' : 'block';
}

// static/js/main.js (actualizar la función sendMessage)
function sendMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();
    if (message === '') return;

    const chatbotBody = document.getElementById('chatbot-body');
    const userMessage = document.createElement('div');
    userMessage.className = 'chatbot-message user';
    userMessage.textContent = message;
    chatbotBody.appendChild(userMessage);

    // Mostrar un indicador de "escribiendo"
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'chatbot-message bot typing';
    typingIndicator.textContent = 'Escribiendo...';
    chatbotBody.appendChild(typingIndicator);

    // Simular un retraso para el efecto de escritura
    setTimeout(() => {
        chatbotBody.removeChild(typingIndicator);
        const botMessage = document.createElement('div');
        botMessage.className = 'chatbot-message bot';
        botMessage.textContent = getBotResponse(message);
        chatbotBody.appendChild(botMessage);

        // Desplazar el chat hacia abajo
        chatbotBody.scrollTop = chatbotBody.scrollHeight;
    }, 1000); // Retraso de 1 segundo

    // Limpiar el input
    input.value = '';
}


function getBotResponse(message) {
    message = message.toLowerCase();

    // Respuestas basadas en palabras clave
    if (message.includes('hola') || message.includes('buenos días') || message.includes('buenas tardes')) {
        return '¡Hola! ¿En qué puedo ayudarte hoy?';
    } else if (message.includes('cita') || message.includes('turno') || message.includes('agendar')) {
        return 'Puedes programar una cita en la sección "Citas". ¿Necesitas ayuda con el formulario?';
    } else if (message.includes('producto') || message.includes('artículo') || message.includes('comprar')) {
        return 'Tenemos productos para ganadería, porcicultura, avicultura y mascotas. Visita la sección "Productos" para ver más. ¿Buscas algo en particular?';
    } else if (message.includes('precio') || message.includes('costo') || message.includes('cuánto')) {
        return 'Los precios varían según el producto. Te recomiendo visitar la sección "Productos" para ver los detalles. ¿Hay algo específico que te interese?';
    } else if (message.includes('horario') || message.includes('abren') || message.includes('cierran')) {
        return 'Nuestro horario es de lunes a viernes de 8:00 AM a 6:00 PM, y los sábados de 9:00 AM a 2:00 PM. ¿Te gustaría agendar una cita?';
    } else if (message.includes('ubicación') || message.includes('dónde están') || message.includes('dirección')) {
        return 'Estamos ubicados en Alcalá, Valle del Cauca, Colombia. Puedes ver más detalles en la sección "Contacto". ¿Necesitas indicaciones?';
    } else if (message.includes('contacto') || message.includes('teléfono') || message.includes('correo')) {
        return 'Puedes contactarnos al +57 312 345 6789 o por correo a contacto@elgalpon.com. También puedes usar el formulario en la sección "Contacto". ¿En qué puedo ayudarte?';
    } else if (message.includes('gracias') || message.includes('bye') || message.includes('adios')) {
        return '¡De nada! Si necesitas algo más, aquí estaré. ¡Hasta pronto!';
    } else if (message.includes('quién eres') || message.includes('qué eres')) {
        return 'Soy el asistente virtual de El Galpón, una tienda veterinaria en Alcalá, Valle del Cauca. Estoy aquí para ayudarte con cualquier pregunta sobre nuestros productos, citas, o servicios. ¿En qué puedo ayudarte?';
    } else if (message.includes('ayuda') || message.includes('necesito')) {
        return '¡Claro que sí! Puedo ayudarte con citas, productos, horarios, o cualquier otra consulta. ¿Qué necesitas?';
    } else {
        // Respuesta predeterminada para preguntas no reconocidas
        return 'Lo siento, no entendí tu pregunta. ¿Puedes reformularla? Estoy aquí para ayudarte con citas, productos, horarios, y más.';
    }
}
// Back to Top Button
window.addEventListener('scroll', () => {
    const backToTop = document.getElementById('back-to-top');
    if (window.scrollY > 300) {
        backToTop.classList.add('show');
    } else {
        backToTop.classList.remove('show');
    }
});

document.getElementById('back-to-top')?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    displayCart();
    document.querySelectorAll('[id^="favorite-"]').forEach(button => {
        const productId = parseInt(button.id.split('-')[1]);
        if (favorites.includes(productId)) {
            button.classList.add('favorited');
        }
    });
    document.querySelectorAll('[id^="reviews-"]').forEach(container => {
        const productId = parseInt(container.id.split('-')[1]);
        displayReviews(productId);
    });
});

// static/js/main.js (añadir al final)
// Inicializar el mapa
function initMap() {
    const location = { lat: 4.6747, lng: -75.7817 }; // Coordenadas de Alcalá, Valle del Cauca
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: location,
    });
    new google.maps.Marker({
        position: location,
        map: map,
        title: "El Galpón",
    });
}

// Mostrar el botón de volver arriba al hacer scroll
window.onscroll = function() {
    const backToTop = document.getElementById('back-to-top');
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        backToTop.style.display = 'block';
    } else {
        backToTop.style.display = 'none';
    }
};

// Volver arriba al hacer clic
document.getElementById('back-to-top').onclick = function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
};

// Ocultar el loader cuando la página esté cargada
window.onload = function() {
    const loader = document.getElementById('loader');
    loader.classList.add('hidden');
};