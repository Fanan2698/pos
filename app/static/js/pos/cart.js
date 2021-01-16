let products = [
  {
    id: 1,
    name: 'kue',
    price: 15000,
    stock: 10,
    category: 1
  },
  {
    id: 2,
    name: 'susu',
    price: 10000,
    stock: 10,
    category: 2
  },

]

let carts = document.querySelectorAll('.add-cart');

for (let i=0; i < carts.length; i++) {
  // when click carts
  carts[i].addEventListener('click', () => {
    // call cartNumber function
    cartNumber(products[i]);
  })
}

function onLoadCartNumber() {
  // load cart number when refresh / first load
  let productNumbers = localStorage.getItem('cartNumbers');

  if(productNumbers) {
    document.querySelector('.cart span').textContent = productNumbers;
  }
}

function cartNumber(product) {
  // get data from localstorage
  let productNumbers = localStorage.getItem('cartNumbers');

  // parse from string to int
  productNumbers = parseInt(productNumbers);

  if(productNumbers) {
    // save to cart to localstorage and plus 1
    localStorage.setItem('cartNumbers', productNumbers + 1);
    document.querySelector('.cart span').textContent = productNumbers + 1;
  } else {
    // no items in cart, set 1
    localStorage.setItem('cartNumbers', 1);
    document.querySelector('.cart span').textContent = 1;
  }

  setItems(product);

}

function setItems(product) {
  console.log("My Product is", product)
}

onLoadCartNumber();
