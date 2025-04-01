// static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.add('hidden');
    }

    // Modo oscuro
    const themeSwitch = document.getElementById('theme-switch');
    themeSwitch.addEventListener('change', () => {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
    });

    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        themeSwitch.checked = true;
    }

    // Partículas
    particlesJS('particles-js', {
        particles: {
            number: { value: 80, density: { enable: true, value_area: 800 } },
            color: { value: '#A9CBA4' },
            shape: { type: 'circle' },
            opacity: { value: 0.5, random: false },
            size: { value: 3, random: true },
            line_linked: { enable: true, distance: 150, color: '#A9CBA4', opacity: 0.4, width: 1 },
            move: { enable: true, speed: 2, direction: 'none', random: false, straight: false, out_mode: 'out', bounce: false }
        },
        interactivity: {
            detect_on: 'canvas',
            events: { onhover: { enable: true, mode: 'repulse' }, onclick: { enable: true, mode: 'push' }, resize: true },
            modes: { repulse: { distance: 100, duration: 0.4 }, push: { particles_nb: 4 } }
        },
        retina_detect: true
    });

    // Mapa
    window.initMap = function() {
        const location = { lat: 4.6743, lng: -75.7661 }; // Coordenadas de Alcalá, Valle del Cauca
        const map = new google.maps.Map(document.getElementById('map'), {
            zoom: 15,
            center: location
        });
        new google.maps.Marker({
            position: location,
            map: map,
            title: 'El Galpón'
        });
    };
});

let products = [];
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function loadProducts() {
    const productList = document.getElementById('product-list');
    const featuredProductList = document.getElementById('featured-product-list');
    const targetList = productList || featuredProductList;

    if (!targetList) return;

    targetList.innerHTML = '<p>Cargando productos...</p>';

    fetch('/api/products/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            products = data;
            displayProducts(products, targetList);
            if (featuredProductList) {
                displayProducts(products.slice(0, 4), featuredProductList); // Mostrar solo 4 productos destacados
            }
        })
        .catch(error => {
            targetList.innerHTML = '<p>Error al cargar los productos.</p>';
            console.error('Error:', error);
        });
}

function displayProducts(productsToShow, targetList) {
    targetList.innerHTML = '';
    if (productsToShow.length === 0) {
        targetList.innerHTML = '<p>No se encontraron productos.</p>';
        return;
    }

    productsToShow.forEach(product => {
        const div = document.createElement('div');
        div.className = 'product animate__animated animate__fadeIn';
        const imageUrl = product.image ? `${window.location.origin}${product.image}` : '/static/images/placeholder.jpg';
        div.innerHTML = `
            <img src="${imageUrl}" alt="${product.name}" loading="lazy">
            <h3>${product.name}</h3>
            <p>${product.description}</p>
            <p>Precio: $${product.price.toFixed(2)}</p>
            <button onclick="addToCart(${product.id})">Añadir al Carrito</button>
        `;
        targetList.appendChild(div);
    });
}

function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    cart.push(product);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();

    // Animación de "volar al carrito"
    const cartIcon = document.getElementById('cart-count');
    const productElement = event.target.parentElement;
    const productImage = productElement.querySelector('img');
    const flyingImage = productImage.cloneNode(true);
    flyingImage.style.position = 'absolute';
    flyingImage.style.width = '50px';
    flyingImage.style.zIndex = '2000';
    flyingImage.style.transition = 'all 1s ease';
    document.body.appendChild(flyingImage);

    const startRect = productImage.getBoundingClientRect();
    const endRect = cartIcon.getBoundingClientRect();

    flyingImage.style.left = startRect.left + 'px';
    flyingImage.style.top = startRect.top + 'px';

    setTimeout(() => {
        flyingImage.style.left = endRect.left + 'px';
        flyingImage.style.top = endRect.top + 'px';
        flyingImage.style.opacity = '0';
        flyingImage.style.transform = 'scale(0.2)';
    }, 50);

    setTimeout(() => {
        flyingImage.remove();
    }, 1000);
}

function updateCartCount() {
    const cartCount = document.getElementById('cart-count');
    cartCount.textContent = cart.length;
}

// Mostrar productos en el carrito
function displayCart() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    if (!cartItems || !cartTotal) return;

    cartItems.innerHTML = '';
    if (cart.length === 0) {
        cartItems.innerHTML = '<p>Tu carrito está vacío.</p>';
        cartTotal.textContent = '';
        return;
    }

    let total = 0;
    cart.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'product animate__animated animate__fadeIn';
        const imageUrl = item.image ? `${window.location.origin}${item.image}` : '/static/images/placeholder.jpg';
        div.innerHTML = `
            <img src="${imageUrl}" alt="${item.name}" loading="lazy">
            <h3>${item.name}</h3>
            <p>Precio: $${item.price.toFixed(2)}</p>
            <button onclick="removeFromCart(${index})">Eliminar</button>
        `;
        cartItems.appendChild(div);
        total += parseFloat(item.price);
    });

    cartTotal.textContent = `Total: $${total.toFixed(2)}`;
}

// Eliminar producto del carrito
function removeFromCart(index) {
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    displayCart();
}

// Vaciar carrito
function clearCart() {
    cart = [];
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    displayCart();
}

// Manejo del formulario de citas con AJAX
const appointmentForm = document.getElementById('appointment-form');
if (appointmentForm) {
    appointmentForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const formData = new FormData(appointmentForm);
        fetch(appointmentForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const successMessage = document.createElement('p');
                successMessage.style.color = 'green';
                successMessage.textContent = '¡Cita agendada con éxito! Te contactaremos pronto.';
                appointmentForm.parentElement.insertBefore(successMessage, appointmentForm);
                appointmentForm.reset();
            } else {
                const errorMessage = document.createElement('p');
                errorMessage.style.color = 'red';
                errorMessage.textContent = 'Hubo un error al agendar la cita. Por favor, revisa los datos.';
                appointmentForm.parentElement.insertBefore(errorMessage, appointmentForm);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const errorMessage = document.createElement('p');
            errorMessage.style.color = 'red';
            errorMessage.textContent = 'Error al procesar la solicitud. Intenta de nuevo.';
            appointmentForm.parentElement.insertBefore(errorMessage, appointmentForm);
        });
    });
}

// Cargar productos y carrito al iniciar
if (document.getElementById('product-list') || document.getElementById('featured-product-list')) {
    loadProducts();
}

if (document.getElementById('cart-items')) {
    displayCart();
}

const clearCartButton = document.getElementById('clear-cart');
if (clearCartButton) {
    clearCartButton.addEventListener('click', clearCart);
}

updateCartCount();