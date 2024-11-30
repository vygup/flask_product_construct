const products = [];
const nadb_price = [];

// Получаем список названий из JSON
const yourListOfValues = JSON.parse($('#yourListOfValues').text());

// Проверяем наличие названия в списке
function isProductValid(product) {
    return yourListOfValues.includes(product);
}

// Обработка введенного пользователем названия и к-ва
function addProduct() {
    const productInput = document.getElementById('product');
    const quantityInput = document.getElementById('quantity');

    const product = productInput.value;
    const quantity = quantityInput.value;

    // Проверка на пустоту и на соответсвие списку названий
    if (product.trim() !== '' && quantity > 0 && isProductValid(product)) {
        products.push({ product: product, quantity: quantity });
        productInput.value = '';
        quantityInput.value = '';
        displayProducts();
    } else {
        alert('Введите существующее название и количество.');
    }
}


// Отображение списка добавленных продуктов
function displayProducts() {
    const productList = document.getElementById('productList');
    productList.innerHTML = '';

    products.forEach((item, index) => {
        const li = document.createElement('li');
        li.textContent = `${item.product} - ${item.quantity}`;

        // Кнопка удаления для каждого сохраненного значения
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'X';
        deleteButton.onclick = () => deleteProduct(index);
        deleteButton.style.marginLeft = '10px'; // Добавляем отступ слева
        deleteButton.style.color = 'red'; // Установка красного цвета


        li.appendChild(deleteButton);
        productList.appendChild(li);
    });
}

// Функция удаления сохраненного значения из списка
function deleteProduct(index) {
    products.splice(index, 1);
    displayProducts();
}

// Отправка данных в Python
function submitProducts() {
    if (products.length > 0) {

        // Отправка данных в python Flask
        $.ajax({
            type: "POST",
            url: "/save_product",
            data: JSON.stringify(products),
            contentType: "application/json",
            success: function(response) {
                console.log("Product data sent to server successfully!");
            }
        });

        window.location.href = '/final_info';

        // Очистим список продуктов
        products = [];
        // displayProducts();
        

    } else {
        alert('Добавьте как минимум один продукт перед отправкой.');
    }
}


// Обработка введенного пользователем названия и к-ва
function price_refresh() {
    const nadbpriceInput = document.getElementById('price_nadb');
    const salenadbInput = document.getElementById('sale_nadb');

    const nadbprice = nadbpriceInput.value;
    const salenadb = salenadbInput.value;

    // Проверка на пустоту и на соответсвие списку названий
    if (nadbprice >= 0 && salenadb >= 0) {
        nadb_price.push({ nadbprice: nadbprice, salenadb:salenadb});
        nadbpriceInput.value = 0;
        salenadbInput.value = 0;

        $.ajax({
            type: "POST",
            url: "/save_val",
            data: JSON.stringify(nadb_price),
            contentType: "application/json",
            success: function(response) {
                console.log("Product data sent to server successfully!");
            }
        });

        // window.location.href = '/final_info';

        location.reload();

    } else {
        alert('Введите корректное значение.');
    }
}
