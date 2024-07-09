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
        if (data.success) {
          updateCartIcon(data.cartCount);
        }
        console.log('Item added to cart successfully');
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    });
  }
}

function updateCartIcon(count) {
  const cartCountElement = document.getElementById('cart-count');
  if (cartCountElement) {
    cartCountElement.textContent = count;
  }
  
  const cartIcon = document.getElementById('cart-icon');
  if (cartIcon) {
    cartIcon.setAttribute('data-count', count);
  }
}

// Function to initialize the cart count
function initializeCartCount() {
  fetch('/get_cart_count')
    .then(response => response.json())
    .then(data => {
      updateCartIcon(data.cartCount);
    })
    .catch(error => console.error('Error initializing cart count:', error));
}

  addToCartBtns();
  initializeCartCount();
  updateCartIcon(count);




