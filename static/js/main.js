const hamburgerlist = document.getElementById("burgerlist");
const navbar = document.getElementById("navbar");
const unshowlist = document.getElementById("unshowlist")

const noAnimationElements = document.querySelectorAll(".noAnimation");

const alerts = document.querySelectorAll('.alert');

const quantityInput = document.getElementById('quantity');
const decreaseBtn = document.querySelector('.decrease');
const increaseBtn = document.querySelector('.increase');


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

  
decreaseBtn.addEventListener('click', () => {
    if (quantityInput.value > 1) {
    quantityInput.value = parseInt(quantityInput.value) - 1;
    }
});

increaseBtn.addEventListener('click', () => {
    if (quantityInput.value < 100) {
    quantityInput.value = parseInt(quantityInput.value) + 1;
    }
});

quantityInput.addEventListener('change', () => {
    if (quantityInput.value < 1) {
    quantityInput.value = 1;
    } else if (quantityInput.value > 100) {
    quantityInput.value = 100;
    }
})

alerts.forEach(function(alert) {
  setTimeout(function() {
    alert.classList.add('fade-out');
    setTimeout(function() {
        alert.remove();
    }, 1500);
  }, 2000);
});