const sliders = document.querySelectorAll(".slider");
const btns = document.querySelectorAll(".btn");
const bar = document.querySelector(".hamburger");
const sideNav = document.querySelector("nav ul");
let flag = false ;
let active = 1;

//==> this function will reset the slide by removing class "active"
function resetSlide() {
    sliders.forEach((slider, index) => {
        slider.classList.remove("active");
    });
    btns.forEach((btn, index) => {
        btn.classList.remove("active");
    });
}

//==> this callback function will change the slide automatically after every 5s .
setInterval(() => {
    resetSlide();
    if (active == sliders.length) {
        active = 0;
    }
    sliders[active].classList.add("active");
    btns[active].classList.add("active");
    active = active + 1;
}, 5000);

//==> Adding event listener to the buttons
btns.forEach((btn, index) => {
    btn.addEventListener("click", (e)=>{handleSlide(e,index)});
});

//==> this function will manually set the slide as per users click event .
function handleSlide(e , index) {
    resetSlide();
    sliders[index].classList.add("active");
    btns[index].classList.add("active");
    active = index ;
}

bar.addEventListener("click" , handleSideNav)
function handleSideNav(e){
    flag = !flag ;
    if(flag)
    {
        e.target.setAttribute("class" , "fa-solid fa-xmark hamburger");
        sideNav.style.left = "0";
    }
    else{
        e.target.setAttribute("class" , "fa-solid fa-bars hamburger");
        sideNav.style.left = "-35vw";
    }
}
