document.addEventListener('DOMContentLoaded', () => {
    const productList = document.getElementById('product-list');
    const cartElement = document.getElementById('cart');
    const cartTotalElement = document.getElementById('cart-total');
    const checkoutButton = document.createElement('button');
    let cart = [];
    let products = [];

    const apiURL = '/producto';

    checkoutButton.textContent = 'Pagar';
    checkoutButton.onclick = () => {
        const totalAmount = cart.reduce((sum, item) => sum + item.valor_producto * item.quantity, 0);
        window.location.href = `/create_transaction?amount=${totalAmount}`;
    };

    cartTotalElement.after(checkoutButton);

    const fetchProducts = async () => {
        try {
            const response = await fetch(apiURL);
            if (!response.ok) {
                throw new Error('Error al obtener los productos');
            }
            products = await response.json();
            displayProducts(products);
        } catch (error) {
            console.error(error);
            productList.innerHTML = '<p>Error al cargar los productos</p>';
        }
    };

    const displayProducts = (products) => {
        products.forEach(product => {
            const productElement = document.createElement('div');
            productElement.classList.add('product');
            productElement.innerHTML = `
                <img src="${product.image}" alt="${product.nombre_producto}">
                <h2>${product.nombre_producto}</h2>
                <p>Tipo: ${product.tipo_producto}</p>
                <p>Precio: $${product.valor_producto}</p>
                <button onclick="addToCart(${product.id_producto})">Añadir al Carrito</button>
            `;
            productList.appendChild(productElement);
        });
    };

    window.addToCart = (id_producto) => {
        const product = products.find(p => p.id_producto === id_producto);
        const existingItem = cart.find(item => item.id_producto === id_producto);

        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({ ...product, quantity: 1 });
        }

        displayCart();
    };

    const updateQuantity = (id_producto, quantity) => {
        const item = cart.find(item => item.id_producto === id_producto);
        if (item) {
            item.quantity = parseInt(quantity);
            if (item.quantity <= 0) {
                item.quantity = 1;  // Prevent quantity from being zero or negative
            }
            displayCart();
        }
    };

    const displayCart = () => {
        cartElement.innerHTML = '';
        cart.forEach(item => {
            const cartItemElement = document.createElement('div');
            cartItemElement.classList.add('cart-item');
            cartItemElement.innerHTML = `
                <h3>${item.nombre_producto}</h3>
                <p>Precio: $${item.valor_producto}</p>
                <p>Cantidad: <input type="number" value="${item.quantity}" min="1" onchange="updateQuantity(${item.id_producto}, this.value)"></p>
            `;
            cartElement.appendChild(cartItemElement);
        });

        const total = cart.reduce((sum, item) => sum + item.valor_producto * item.quantity, 0);
        cartTotalElement.innerHTML = `<h2>Total: $${total.toFixed(2)}</h2>`;
    };

    fetchProducts();
});
