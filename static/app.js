document.addEventListener('DOMContentLoaded', () => {
    const productList = document.getElementById('product-list');
    const cartElement = document.getElementById('cart');
    const cartTotalElement = document.getElementById('cart-total');
    const checkoutButton = document.createElement('button');
    let cart = [];
    let products = [];

    const apiURL = '/producto';

    checkoutButton.textContent = 'Pagar';
    checkoutButton.disabled = true;  // Inicialmente deshabilitado
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
        productList.innerHTML = '';  // Limpiar la lista de productos antes de mostrar
        products.forEach(product => {
            const productElement = document.createElement('div');
            productElement.classList.add('product');
            productElement.innerHTML = `
                <img src="https://media.istockphoto.com/id/1351998505/es/foto/herramientas-puestas-a-la-venta-en-una-ferreter%C3%ADa.jpg?s=612x612&w=0&k=20&c=WwqYmIhbr18RnWAqWKnEm_CV_9NBCmEZcqqHTrXsZiA=" alt="${product.nombre_producto}">
                <h2>${product.nombre_producto}</h2>
                <p>Tipo: ${product.tipo_producto}</p>
                <p>Precio CLP: $${product.valor_producto}</p>
                <p>Precio USD: $${product.valor_producto_usd}</p>
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

    window.updateQuantity = (id_producto, quantity) => {
        const item = cart.find(item => item.id_producto === id_producto);
        if (item) {
            item.quantity = parseInt(quantity);
            if (item.quantity <= 0) {
                item.quantity = 1;  // Prevenir que la cantidad sea cero o negativa
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
                <p>Precio CLP: $${item.valor_producto}</p>
                <p>Precio USD: $${item.valor_producto_usd}</p>
                <p>Cantidad: <input type="number" value="${item.quantity}" min="1" onchange="updateQuantity(${item.id_producto}, this.value)"></p>
            `;
            cartElement.appendChild(cartItemElement);
        });

        const totalCLP = cart.reduce((sum, item) => sum + item.valor_producto * item.quantity, 0);
        const totalUSD = cart.reduce((sum, item) => sum + item.valor_producto_usd * item.quantity, 0);
        cartTotalElement.innerHTML = `<h2>Total: $${totalCLP.toFixed(2)} CLP / $${totalUSD.toFixed(2)} USD</h2>`;

        // Habilitar o deshabilitar el botón de pago
        checkoutButton.disabled = cart.length === 0;
    };

    fetchProducts();
});
