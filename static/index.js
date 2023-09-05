const addProductButton = document.getElementById("addProduct");
const removeProductButton = document.getElementById("removeProduct");
const productsDiv = document.getElementById("products");
const productItem = document.querySelector(".product-item");

// Initialize the product counter
let productCounter = 1;

// Add products
addProductButton.addEventListener("click", () => {
  if (productCounter < 3) {
    const newProductItem = productItem.cloneNode(true);
    productsDiv.appendChild(newProductItem);
    productCounter++;
  }
});

// Remove products
removeProductButton.addEventListener("click", () => {
  if (productCounter > 1) {
    const productItems = document.querySelectorAll(".product-item");
    const lastProductItem = productItems[productItems.length - 1];
    productsDiv.removeChild(lastProductItem);
    productCounter--;
  }
});