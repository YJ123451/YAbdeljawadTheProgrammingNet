document.addEventListener('DOMContentLoaded', function () {
    let themeButton = document.getElementById("theme-button");
    const toggleDarkMode = () => {
      var element = document.body;
      element.classList.toggle("dark-mode");
    }
    themeButton.addEventListener("click", toggleDarkMode);

    // Open Stack Overflow
    let stackButton = document.getElementById("Stack");
    const stack = () => {
      window.open("https://stackoverflow.com/");
    }
    stackButton.addEventListener("click", stack);

    // Open Codepath
    let CodePathButton = document.getElementById("Codepath");
    function cp() {
      window.open("https://www.codepath.org/");
    }
    CodePathButton.addEventListener("click", cp);

    // Signature Form
    let count = 3;
   let signNowButton = document.getElementById("sign-now-button");
  const addSignature = (person) => {
    // let name = person.name.value;
    // let hometown = document.getElementById("hometown").value;
    // let signatures = document.getElementById("signatures");
    let newSignature = document.createElement("p");
    newSignature.textContent = `🖊️ ${person.name} from ${person.hometown}  supports this.`;
    signatures.appendChild(newSignature);
    

    let counter = document.getElementById("counter");
    counter.remove();
    count = count + 1;
    counter = document.createElement("p");
    counter.id = "counter";
    counter.innerText = "🖊️" + count + " people have signed this petition and support this cause."
    signatures.appendChild(counter);
  };

  // TODO: Remove the click event listener that calls addSignature()

  // TODO: Complete validation form



  
  const validateForm = (event) => {
    event.preventDefault();
      let containsErrors = false;
    let petitionInputs = document.getElementById("petition-form").querySelectorAll('input, select, textarea');
      console.log("Petition Inputs:", petitionInputs);
    let person = {
      name:petitionInputs[0].value, 
      hometown:petitionInputs[2].value,
      email:petitionInputs[1].value
    }
      for (let i = 0; i < petitionInputs.length; i++) {
          console.log("Input value:", petitionInputs[i].value);
          if (person.hometown.length < 2) {
            containsErrors = true;  
            petitionInputs[i].classList.add('error');
                     } 
          else {
      petitionInputs[i].classList.remove('error');
          }
      }
    const email = document.getElementById('email');
      if (!email.value.includes('.com') && !email.value.includes('.org') && !email.value.includes('.net') && !email.value.includes('.edu') && !email.value.includes('.gov')){
        containsErrors = true;
        alert("Please enter a valid email address.")
        email.classList.add('error');
      }
      else{
        email.classList.remove('error');
      }

      if (containsErrors == false) {
          addSignature(person);
          toggleModal(person);
          for (let i = 0; i < petitionInputs.length; i++) {
              petitionInputs[i].value = "";
              containsErrors = false;
          }
      }
   
  }
  const toggleModal = (person)=>{
    let modal = document.getElementById('thanks-modal');
    let modalContent = document.getElementById('thanks-modal-content');
    modalContent.innerText = `Thank you for your support ${person.name}!`;
    modal.style.display = 'flex';
    setTimeout(()=>{
      modal.style.display = 'none';
    }, 5000)
  }
   
    signNowButton.addEventListener('click', validateForm);
});
document.addEventListener('scroll',function() {
let animation ={
  revealDistance: 150,
  initialOpacity: 0,
  transitionDelay: 0,
  transitionDuration: '2s',
  transitionProperty: 'all',
  transitionTimingFunction: 'ease'
}
let revealableContainers = document.querySelectorAll('.revealable');
const reveal = ()=>{
  for(let i = 0; i < revealableContainers.length; i++){
    let windowHeight = window.innerHeight;
    let topOfRevealableContainer = revealableContainers[i].getBoundingClientRect().top;
    if(topOfRevealableContainer < windowHeight - animation.revealDistance){
      revealableContainers[i].classList.add('active');
    }
    else{
      revealableContainers[i].classList.remove('active');
    }
  }
}
window.addEventListener('scroll', reveal);
let closeButton = document.getElementById('Close-Modal');
const closeModal =() =>{
  let modal = document.getElementById('thanks-modal');
  modal.style.display = 'none';
}
  closeButton.addEventListener('click',closeModal);
});