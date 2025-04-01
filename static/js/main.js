// static/js/main.js (actualizado con Intersection Observer)

// Loader
window.addEventListener('load', () => {
    const loader = document.getElementById('loader');
    loader.classList.add('hidden');
});

// Dark Mode Toggle
document.getElementById('theme-switch').addEventListener('change', () => {
    document.body.classList.toggle('dark-mode');
});

// Particles.js for Hero Section
if (document.getElementById('particles-js')) {
    particlesJS('particles-js', {
        particles: {
            number: { value: 80, density: { enable: true, value_area: 800 } },
            color: { value: '#A9CBA4' },
            shape: { type: 'circle' },
            opacity: { value: 0.5, random: false },
            size: { value: 3, random: true },
            line_linked: { enable: true, distance: 150, color: '#A9CBA4', opacity: 0.4, width: 1 },
            move: { enable: true, speed: 6, direction: 'none', random: false, straight: false, out_mode: 'out', bounce: false }
        },
        interactivity: {
            detect_on: 'canvas',
            events: { onhover: { enable: true, mode: 'repulse' }, onclick: { enable: true, mode: 'push' }, resize: true },
            modes: { repulse: { distance: 100, duration: 0.4 }, push: { particles_nb: 4 } }
        },
        retina_detect: true
    });
}

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

function addToCart(productId) {
    cart.push(productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    showToast('Producto añadido al carrito', 'success');
}

function updateCartCount() {
    const cartCount = document.getElementById('cart-count');
    cartCount.textContent = cart.length;
}

// Favoritos
let favorites = JSON.parse(localStorage.getItem('favorites')) || [];

function toggleFavorite(productId) {
    const button = document.getElementById(`favorite-${productId}`);
    if (favorites.includes(productId)) {
        favorites = favorites.filter(id => id !== productId);
        button.classList.remove('favorited');
        showToast('Producto eliminado de favoritos', 'error');
    } else {
        favorites.push(productId);
        button.classList.add('favorited');
        showToast('Producto añadido a favoritos', 'success');
    }
    localStorage.setItem('favorites', JSON.stringify(favorites));
}

// Inicializar favoritos al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.favorite-button').forEach(button => {
        const productId = parseInt(button.id.replace('favorite-', ''));
        if (favorites.includes(productId)) {
            button.classList.add('favorited');
        }
    });
});

// Filtros y Búsqueda
function applyFilters() {
    const search = document.getElementById('search-input')?.value || '';
    const categoria = document.getElementById('categoria-filter')?.value || '';
    const especie = document.getElementById('especie-filter')?.value || '';
    const sort = document.getElementById('sort-filter')?.value || '';

    const params = new URLSearchParams();
    if (search) params.set('search', search);
    if (categoria) params.set('categoria', categoria);
    if (especie) params.set('especie', especie);
    if (sort) params.set('sort', sort);

    window.location.href = `/products/?${params.toString()}`;
}

document.getElementById('search-input')?.addEventListener('input', applyFilters);
document.getElementById('categoria-filter')?.addEventListener('change', applyFilters);
document.getElementById('especie-filter')?.addEventListener('change', applyFilters);
document.getElementById('sort-filter')?.addEventListener('change', applyFilters);

// Vista Rápida
function openQuickView(productId) {
    fetch(`/api/productos/${productId}/`)
        .then(response => response.json())
        .then(data => {
            const content = `
                <img src="${data.imagen || '/static/images/placeholder.jpg'}" alt="${data.nombre}">
                <h3>${data.nombre}</h3>
                <p>${data.descripcion}</p>
                <p>Categoría: ${data.categoria}</p>
                <p>Especie: ${data.especie}</p>
                <p>Precio: $${data.precio}</p>
                <p>Stock: ${data.stock}</p>
                <button onclick="addToCart(${data.id})">Añadir al Carrito</button>
            `;
            document.getElementById('quick-view-content').innerHTML = content;
            document.getElementById('quick-view-modal').style.display = 'flex';
        })
        .catch(error => {
            console.error('Error al cargar el producto:', error);
            showToast('Error al cargar el producto', 'error');
        });
}

function closeQuickView() {
    document.getElementById('quick-view-modal').style.display = 'none';
}

// Compartir Producto
function shareProduct(name, url) {
    if (navigator.share) {
        navigator.share({
            title: `Mira este producto: ${name}`,
            url: url
        }).then(() => {
            showToast('Producto compartido con éxito', 'success');
        }).catch(error => {
            console.error('Error al compartir:', error);
            showToast('Error al compartir el producto', 'error');
        });
    } else {
        navigator.clipboard.writeText(url).then(() => {
            showToast('Enlace copiado al portapapeles', 'success');
        }).catch(error => {
            console.error('Error al copiar el enlace:', error);
            showToast('Error al copiar el enlace', 'error');
        });
    }
}

// Notificaciones
function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.getElementById('toast-container').appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Chatbot
function toggleChatbot() {
    const chatbotWindow = document.getElementById('chatbot-window');
    chatbotWindow.style.display = chatbotWindow.style.display === 'block' ? 'none' : 'block';
}

function sendMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();
    if (!message) return;

    // Añadir mensaje del usuario
    const userMessage = document.createElement('div');
    userMessage.className = 'chatbot-message user';
    userMessage.textContent = message;
    document.getElementById('chatbot-body').appendChild(userMessage);

    // Limpiar input
    input.value = '';

    // Respuesta del bot
    setTimeout(() => {
        const botMessage = document.createElement('div');
        botMessage.className = 'chatbot-message bot';
        botMessage.textContent = getBotResponse(message);
        document.getElementById('chatbot-body').appendChild(botMessage);

        // Desplazar hacia abajo
        const chatbotBody = document.getElementById('chatbot-body');
        chatbotBody.scrollTop = chatbotBody.scrollHeight;
    }, 500);
}

// Continuación desde getBotResponse
function getBotResponse(message) {
    message = message.toLowerCase();
    if (message.includes('hola') || message.includes('buenos días') || message.includes('buenas tardes')) {
        return '¡Hola! ¿En qué puedo ayudarte hoy?';
    } else if (message.includes('productos') || message.includes('qué venden')) {
        return 'Vendemos productos para el cuidado de animales, como alimentos, medicamentos y accesorios. Puedes ver todos nuestros productos en la sección de "Productos".';
    } else if (message.includes('cita') || message.includes('veterinario')) {
        return 'Puedes agendar una cita veterinaria en la sección de "Citas". Solo llena el formulario y te contactaremos para confirmar.';
    } else if (message.includes('ubicación') || message.includes('dónde están')) {
        return 'Estamos ubicados en Alcalá, Valle del Cauca. Puedes ver nuestra ubicación exacta en la sección de "Contacto".';
    } else if (message.includes('horario') || message.includes('a qué hora abren')) {
        return 'Abrimos de lunes a sábado de 8:00 AM a 6:00 PM. Los domingos estamos cerrados.';
    } else if (message.includes('gracias') || message.includes('adiós')) {
        return '¡De nada! Si necesitas más ayuda, aquí estaré. ¡Hasta pronto!';
    } else {
        return 'Lo siento, no entendí tu pregunta. ¿Puedes reformularla? También puedes visitar nuestras secciones de "Productos", "Citas" o "Contacto" para más información.';
    }
}

// Carrusel de Imágenes
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

if (slides.length > 0) {
    showSlide(currentSlide);
    setInterval(nextSlide, 5000); // Cambia cada 5 segundos
}

document.getElementById('next-slide')?.addEventListener('click', nextSlide);
document.getElementById('prev-slide')?.addEventListener('click', prevSlide);

// Desplazamiento Suave
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Volver Arriba
const backToTopButton = document.getElementById('back-to-top');
window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        backToTopButton.style.opacity = '1';
        backToTopButton.classList.add('show');
    } else {
        backToTopButton.style.opacity = '0';
        backToTopButton.classList.remove('show');
    }
});

backToTopButton?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Reseñas de Productos
function submitReview(productId) {
    const rating = document.getElementById(`rating-${productId}`).value;
    const comment = document.getElementById(`comment-${productId}`).value;

    if (!rating || !comment) {
        showToast('Por favor, completa todos los campos', 'error');
        return;
    }

    // Simulación de envío de reseña (puedes integrarlo con una API)
    const reviewList = document.getElementById(`reviews-${productId}`);
    const review = document.createElement('div');
    review.className = 'review';
    review.innerHTML = `
        <p><strong>Calificación:</strong> ${rating}/5</p>
        <p>${comment}</p>
        <hr>
    `;
    reviewList.appendChild(review);

    // Limpiar formulario
    document.getElementById(`rating-${productId}`).value = '';
    document.getElementById(`comment-${productId}`).value = '';
    showToast('Reseña enviada con éxito', 'success');
}

// Efecto de Fade-In al Hacer Scroll
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate__animated', 'animate__fadeIn');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observar secciones y productos
document.querySelectorAll('.section, .product').forEach(element => {
    observer.observe(element);
});