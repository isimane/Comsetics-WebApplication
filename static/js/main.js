const hamburgerlist = document.getElementById("burgerlist");
const noAnimationElements = document.querySelectorAll(".noAnimation");

const navbar = document.getElementById("navbar");
const unshowlist = document.getElementById("unshowlist")



// const alerts = document.querySelectorAll('.alert');

hamburgerlist.addEventListener("click",() =>{
    console.log(navbar.style.display);

    if(navbar.style.display !== 'block'){
        
        navbar.style.display="block";
        hamburgerlist.style.display="none";
        unshowlist.style.display="block";

    }else{
        navbar.style.display="none";
        
    }
})
unshowlist.addEventListener("click",() =>{

    if(navbar.style.display !=='none'){
        navbar.style.display="none";
        hamburgerlist.style.display="block"
        unshowlist.style.display="none";
    }else{
        navbar.style.display="block";
        
    }
})

if (navbar) {
    navbar.classList.add("animateScroll");
  }
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("animateScroll");
      }
    });
  });
  
  noAnimationElements.forEach((element) => {
    if (element !== navbar) {
      observer.observe(element);
    }
  });

document.addEventListener('DOMContentLoaded', function() {
  const quantityInputs = document.querySelectorAll('.quantity');
  
  quantityInputs.forEach(input => {
      const decreaseButton = input.previousElementSibling;
      const increaseButton = input.nextElementSibling;
      
      decreaseButton.addEventListener('click', () => updateQuantity(input, -1));
      increaseButton.addEventListener('click', () => updateQuantity(input, 1));
      input.addEventListener('change', () => validateInput(input));
  });
});

function updateQuantity(input, change) {
  let value = parseInt(input.value) + change;
  value = Math.max(1, Math.min(value, 100));
  input.value = value;
}

function validateInput(input) {
  let value = parseInt(input.value);
  if (isNaN(value) || value < 1) {
      input.value = 1;
  } else if (value > 100) {
      input.value = 100;
  }
}

// alerts.forEach(function(alert) {
//   setTimeout(function() {
//     alert.classList.add('fade-out');
//     setTimeout(function() {
//         alert.remove();
//     }, 1500);
//   }, 2000);
// });


function updateCartIcon() {
  const cartIcon = document.getElementById('cart-icon');
  if (!cartIcon) {
    console.error('Cart icon element not found');
    return;
  }
  fetch('/get_cart_count')
    .then(response => response.json())
    .then(data => {
      const currentCount = data.cartCount;
      cartIcon.setAttribute('data-count', currentCount);
      const counter = cartIcon.querySelector('.cart-count');
      if (counter) {
        counter.textContent = currentCount;
      } else {
        console.warn('Cart count element not found');
      }
    })
    .catch(error => console.error('Error updating cart icon:', error));
}

function addToCartBtns() {
  const addToCart = document.getElementsByClassName('addToCartBtn');
  for (let button of addToCart) {
    button.addEventListener("click", () => {
      console.log('Add to cart clicked');
      const productId = button.getAttribute('data-product-id');
      let productQuantity;
      if (document.getElementById('product_quantity_' + productId)) {
        productQuantity = document.getElementById('product_quantity_' + productId).value;
      } else {
        productQuantity = 1;
      }
      
      const payload = {
        id: parseInt(productId),
        quantity: parseInt(productQuantity),
      };

      fetch('/add_to_cart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      })
      .then(response => response.json())
      .then(data => {
        console.log('Server response:', data);
        updateCartIcon();
        console.log('Item added to cart successfully');
      })
      .catch((error) => {
        console.error('Error:', error);
       
      });
    });
  }
}
function removeFromCart(productId) {
  fetch('/remove_from_cart', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id: parseInt(productId) })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Server response:', data);
    updateCartIcon();
    // Refresh the cart page
    location.reload();
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

document.addEventListener('DOMContentLoaded', function() {
  const removeButtons = document.getElementsByClassName('remove-from-cart');
  for (let button of removeButtons) {
    button.addEventListener('click', function() {
      const productId = this.getAttribute('data-product-id');
      removeFromCart(productId);
    });
  }
});

addToCartBtns();



