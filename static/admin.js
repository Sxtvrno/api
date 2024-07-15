async function fetchProducts() {
    const response = await fetch('/producto');
    const products = await response.json();
    const tableBody = document.getElementById('product-table-body');
    tableBody.innerHTML = '';
    products.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${product.id_producto}</td>
            <td><input type="text" value="${product.nombre_producto}" data-id="${product.id_producto}" class="edit-nombre"></td>
            <td>
                <select data-id="${product.id_producto}" class="edit-tipo">
                    <option value="Herramientas-Manuales" ${product.tipo_producto === 'Herramientas-Manuales' ? 'selected' : ''}>Herramientas-Manuales</option>
                    <option value="Materiales-Basicos" ${product.tipo_producto === 'Materiales-Basicos' ? 'selected' : ''}>Materiales-Basicos</option>
                    <option value="Equipos-Seguridad" ${product.tipo_producto === 'Equipos-Seguridad' ? 'selected' : ''}>Equipos-Seguridad</option>
                </select>
            </td>
            <td><input type="number" value="${product.valor_producto}" data-id="${product.id_producto}" class="edit-valor"></td>
            <td><input type="number" value="${product.stock}" data-id="${product.id_producto}" class="edit-stock"></td>
            <td>
                <button onclick="editProduct(${product.id_producto})">Editar</button>
                <button onclick="deleteProduct(${product.id_producto})">Eliminar</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}
let productIdCounter = 1;  // Contador global para productos

async function addProduct(event) {
    event.preventDefault();
    const form = event.target;
    const nombre = form.nombre_producto.value;
    const tipo = form.tipo_producto.value;
    const valor = form.valor_producto.value;
    const stock = form.stock.value

    const response = await fetch(`/create/${nombre}/${valor}/${tipo}/${stock}`, { method: 'POST' });
    if (response.ok) {
        fetchProducts();
        form.reset();
    } else {
        alert('Error al agregar producto');
    }
}

async function editProduct(id) {
    const nombre = document.querySelector(`.edit-nombre[data-id="${id}"]`).value;
    const tipo = document.querySelector(`.edit-tipo[data-id="${id}"]`).value;
    const valor = document.querySelector(`.edit-valor[data-id="${id}"]`).value;
    const stock = document.querySelector(`.edit-stock[data-id="${id}"]`).value;

    const response = await fetch(`/update/${id}/${valor}/${stock}`, { method: 'PUT' });
    if (response.ok) {
        fetchProducts();
    } else {
        alert('Error al editar producto');
    }
}

async function deleteProduct(id) {
    const response = await fetch(`/delete/${id}`, { method: 'DELETE' });
    if (response.ok) {
        fetchProducts();
    } else {
        alert('Error al eliminar producto');
    }
}

document.getElementById('add-product-form').addEventListener('submit', addProduct);
fetchProducts();