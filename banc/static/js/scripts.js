/**
* Define a function to navigate betweens form steps.
* It accepts one parameter. That is - step number.
*/
const navigateToFormStep = (stepNumber,step,next) => {
    // Exit the function if any field in the current tab is invalid:
    if (next == 1 && !validateForm(step)) return false;
      /**
      * Hide all form steps.
      */
      document.querySelectorAll(".form-step").forEach((formStepElement) => {
      formStepElement.classList.add("d-none");
      });
      /**
      * Mark all form steps as unfinished.
      */
      document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
      formStepHeader.classList.add("form-stepper-unfinished");
      formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
      });
      /**
      * Show the current form step (as passed to the function).
      */
      document.querySelector("#step-" + stepNumber).classList.remove("d-none");
      /**
      * Select the form step circle (progress bar).
      */
      const formStepCircle = document.querySelector('li[step="' + stepNumber + '"]');
      /**
      * Mark the current form step as active.
      */
      formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
      formStepCircle.classList.add("form-stepper-active");
      /**
      * Loop through each form step circles.
      * This loop will continue up to the current step number.
      * Example: If the current step is 3,
      * then the loop will perform operations for step 1 and 2.
      */
      for (let index = 0; index < stepNumber; index++) {
      /**
      * Select the form step circle (progress bar).
      */
      const formStepCircle = document.querySelector('li[step="' + index + '"]');
      /**
      * Check if the element exist. If yes, then proceed.
      */
      if (formStepCircle) {
      /**
      * Mark the form step as completed.
      */
      formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
      formStepCircle.classList.add("form-stepper-completed");
      }
      }
      };
      /**
      * Select all form navigation buttons, and loop through them.
      */
      document.querySelectorAll(".btn-navigate-form-step").forEach((formNavigationBtn) => {
      /**
      * Add a click event listener to the button.
      */
      formNavigationBtn.addEventListener("click", () => {
      /**
      * Get the value of the step, stepNumber, next.
      */
      const stepNumber = parseInt(formNavigationBtn.getAttribute("step_number"));
      const next = parseInt(formNavigationBtn.getAttribute("next"));
      const step = parseInt(formNavigationBtn.parentElement.parentElement.getAttribute("step"));
      /**
      * Call the function to navigate to the target form step.
      */
      navigateToFormStep(stepNumber,step,next);
      });
      });
  
      function validateForm(step) {
          // This function deals with validation of the form fields
          var x, y, i, valid = true;
          x = document.getElementsByClassName("form-step");

          if(step == 1){
            return true;
          }
          else if(step == 2){
            let fname = document.getElementById('fullname');
            
            if(fname.value == ''){
              fname.className = "invalid";
              // show error message
              let err = document.querySelector('.err1');
              err.classList.remove('hideErr');
              err.innerHTML = "Please fill in your name!";  
            }
            else{
              fname.classList.remove("invalid");
              // hide error message
              let err = document.querySelector('.err1');
              err.classList.add('hideErr');
              err.innerHTML = "l";
              return true;
            }
          }
          else{
            // get a list of input containers for the current tab
            y = x[step].children[1].children;
            console.log(y);
            // A loop that checks every input field in the current tab:
            for (i = 0; i < y.length; i++) {
              // If a field is empty...
              if (y[i].children[0].value == "") {
                // add an "invalid" class to the field:
                y[i].children[0].className = "invalid";
                // show error message
                y[i].children[1].classList.remove('hideErr');
                y[i].children[1].innerHTML = "Please fill out this field.";
                // add error background color and error message on input with type file
                if(y[i].children[0].type == 'file'){
                  y[i].children[0].nextElementSibling.className += " fileError";
                  y[i].children[0].nextElementSibling.nextElementSibling.nextElementSibling.innerHTML = "Please fill out this  field.";
                }
                // and set the current valid status to false:
                valid = false;
              }
              else{
                //remove invalid class if it exists whilst field is no longer empty
                if (y[i].children[0].classList.contains('invalid')){
                  y[i].children[0].classList.remove('invalid');
                }
                // hide error message and set it to empty strings
                  y[i].children[1].classList.add('hideErr');
                  y[i].children[1].innerHTML = "";
                // remove error background color and error text on input with type file
                if(y[i].children[0].type == 'file' && y[i].children[0].nextElementSibling.classList.contains('fileError')){
                  y[i].children[0].nextElementSibling.classList.remove('fileError');
                  y[i].children[0].nextElementSibling.nextElementSibling.nextElementSibling.innerHTML = "";
                }
              }
              //check if email format is valid
              if(y[i].children[0].type == 'email' && y[i].children[0].value != ""){
                // if provided email does not match a valid email format
                var mailformat = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
                if(!y[i].children[0].value.match(mailformat)){
                // add an "invalid" class to the field:
                y[i].children[0].className = "invalid";
                // show error message
                y[i].children[1].classList.remove('hideErr');
                y[i].children[1].innerHTML = "Enter valid email address, with @ symbol";
                  valid = false;
                }
                else{
                //remove invalid class if it exists whilst field has valid email address
                if (y[i].children[0].classList.contains('invalid')){
                  y[i].children[0].classList.remove('invalid');
                }
                // hide error message and set it to empty strings
                  y[i].children[1].classList.add('hideErr');
                  y[i].children[1].innerHTML = "";
                }
                
              }
            }
          
          return valid; // return the valid status
          }

        }

// DISPLAY SELECTED CATEGORY
function displayCategories(){
  // dictionary holding category and its skills
  let categories = {
    "Websites & Software":["php","css","flutter","python","firebase"],
    "Design & Media":["poster","flyer"],
    "Writing & Content":["poster","flyer"],
    "Data Entry & Admin":["poster","flyer"]
  }
  // select container to hold categories
  let categoriesC = document.querySelector('#categoriesContainer')
  // create variable to hold looped list of categories and set it to our categories container
  let categoriesContainer = ''
  Object.entries(categories).forEach(category => {
    let [cat,val] = category
    categoriesContainer += `<div class="step-child-content step-child-content-1" onclick="displaycValue(this)" id="${category}">
                              <span class="icon-desktop"></span>
                              <p>${cat}</p>
                               <span class="icon-angle-right"></span>
                            </div>`
  })
  categoriesC.innerHTML = categoriesContainer
 
}
// DISPLAY CATEGORY SKILLS
function displaycValue(cat){
  // get id value from parameter
  let catStr = cat.id
  // change the id into an array
  let catArray = catStr.split(',')
  // select the headingand change its content to be the first element of the array
  // whcih is the category name
  let categoryHeading = document.querySelector('.category-heading')
  categoryHeading.innerHTML = catArray[0]
  // create a copy of the array by removing the first item(category name), to be left with only list of skills
  let catArray2 = catArray.splice(1)
  // select the container to hold all skills
  let cValueC = document.querySelector('#cValueContainer')
  // create variable to hold looped list of skills and set it to skills container from our html
  let cValueContainer = ''
  catArray2.forEach(skill => {
    cValueContainer += `<div class="step-child-content step-child-content-1" onclick="displaySkills(this)" id="${skill}">
                              <p>${skill}</p>
                              <span class="icon-plus"></span>
                            </div>`
  })
  cValueC.innerHTML = cValueContainer
}
// display selected skills
function displaySkills(skill){
  // increment skills as they are added
  let numSkills = document.querySelector('.numSkills')
  numSkills.innerHTML =  numSkills.value + 1 //change values to integer
  // select the skill from the id
  let skillValue = skill.id
  // select container to hold list of selected skills
  let sContainer = document.querySelector('#skillsContainer')
  // create variable to hold skills
  let skillsContainer = ''
  skillsContainer = `<div class="skill" onclick="removeSkill(this)"><span>${skillValue}</span><span class="remove-skill">&times;</span><input type="hidden" name="skills${skillValue}" value="${skillValue}"/></div>`
  
  //check if there is a p tag 
  if(sContainer.children[0].tagName == 'P'){
    // replace the p tag with the skill
    sContainer.innerHTML = skillsContainer
    // add class with styles to create a grid layout
    sContainer.classList.add('skillsContainer')
  }
  else{
    // append the skills
    sContainer.innerHTML += skillsContainer
  }

}
// REMOVE SKILL
function removeSkill(sk){
  sk.remove()
  // decrement skills as they are removed
  let numSkills = document.querySelector('.numSkills')
  numSkills.innerHTML =  numSkills.value - 1 //change values to integer
}
// PREVIEW SELECTED PROFILE PHOTO
const input = document.querySelector("#upload-photo");
const output = document.querySelector("output");

input.addEventListener("change", function(){
  displayImage()
});

function displayImage(){
  const file = input.files;
  let image = "";
  image = `<div class="image">
                <img src="${URL.createObjectURL(file[0])}" alt="image">
                </div>`
  output.innerHTML = image;
}

// SHOW NEXT CONTENT ON POST A PROJECT
function showNext(btnNext){
  // select all elements that are hidden
  let pd = document.querySelector('.project-description')
  let sr = document.querySelector('.skills-required')
  let pt = document.querySelector('.payment-type')
  let b = document.querySelector('.budget')
  let d = document.querySelector('.deadline')
  
  // check them one by one if they have the hideContent class
  // which has a display of none, remove the class and scroll to that element when we show it
  if(pd.classList.contains('hideContent')){
    //check if project name is not empty then proceed
    if(pd.previousElementSibling.value == ''){
      pd.previousElementSibling.className = "invalid";
      // show error message
      document.querySelector('.errr').classList.remove('hideErr');
      document.querySelector('.errr').innerHTML = "Please fill in the project name!";
    }
    else{
      //hide errors
      pd.previousElementSibling.classList.remove('invalid');
      document.querySelector('.errr').classList.add('hideErr');
      document.querySelector('.errr').innerHTML = "";
      //show next content
      pd.classList.remove('hideContent')
      pd.scrollIntoView();
    }
  }
  else if(sr.classList.contains('hideContent')){
   //check if project description is not empty then proceed
   if(sr.previousElementSibling.children[2].value == ''){
    sr.previousElementSibling.children[2].className = "invalid";
    // show error message
    document.querySelector('.errr1').classList.remove('hideErr');
    document.querySelector('.errr1').innerHTML = "Please fill in the project description!";
  }
  else{
    //hide errors
    sr.previousElementSibling.children[2].classList.remove('invalid');
    document.querySelector('.errr1').classList.add('hideErr');
    document.querySelector('.errr1').innerHTML = "";
    //show next content
    sr.classList.remove('hideContent')
    sr.scrollIntoView();
  }

  }
  else if(pt.classList.contains('hideContent')){
    console.log(pt.previousElementSibling.children[1].children[1])
    //check if project skills are not empty then proceed
   if(pt.previousElementSibling.children[1].children[1].value == ''){
    pt.previousElementSibling.children[1].children[1].className = "invalid";
    // show error message
    document.querySelector('.errr2').classList.remove('hideErr');
    document.querySelector('.errr2').innerHTML = "Please fill in the required skills!";
  }
  else{
    //hide errors
    pt.previousElementSibling.children[1].children[1].classList.remove('invalid');
    document.querySelector('.errr2').classList.add('hideErr');
    document.querySelector('.errr2').innerHTML = "";
    //show next content
    pt.classList.remove('hideContent')
    pt.scrollIntoView();
  }

  }
  else if(b.classList.contains('hideContent')){
    b.classList.remove('hideContent')
    b.scrollIntoView();
  }
  else if(d.classList.contains('hideContent')){
    d.classList.remove('hideContent')
    d.scrollIntoView();
  }
  else{
    console.log(btnNext.previousElementSibling.children[2].children[0])
    //check if deadline is not empty then proceed
   if(btnNext.previousElementSibling.children[2].children[0].value == ''){
    btnNext.previousElementSibling.children[2].children[0].className = "invalid";
    // show error message
    document.querySelector('.errr3').classList.remove('hideErr');
    document.querySelector('.errr3').innerHTML = "Please fill in the deadline!";
  }
  else{
    //hide errors
    btnNext.previousElementSibling.children[2].children[0].classList.remove('invalid');
    document.querySelector('.errr3').classList.add('hideErr');
    document.querySelector('.errr3').innerHTML = "";
    // submit data
    // change btn type type submit
    btnNext.type = 'submit'
    alert("Project posted successfully!")
  }



    
  }
}

// SHOW MODAL
function showModal(){
  let overlay = document.querySelector('.overlay')
  overlay.classList.add('overlayShow')
}
function showModal2(freelancer){
  let overlay = document.querySelector('.overlay')
  overlay.classList.add('overlayShow')
  document.querySelector('.freelancer_id').value = freelancer.id
 
}
// CLOSE MODAL
function closeModal(){
  let overlay = document.querySelector('.overlay')
  overlay.classList.remove('overlayShow')
}
// CONFIRM BID
function confirmBid(){
  alert("Bid Successful!")
}
// VALIDATE RATING
function validateRating(ratingEl){
  if(ratingEl.value){
    if(ratingEl.value<1){
    document.querySelector('.bid2').type = 'button'
    ratingEl.className = "invalid";
      // show error message
      document.querySelector('.errrat').classList.remove('hideErr');
      document.querySelector('.errrat').innerHTML = "Rating should be from 1 to 5!"; 
  }
  else if(ratingEl.value>5){
    document.querySelector('.bid2').type = 'button'
    ratingEl.className = "invalid";
      // show error message
      document.querySelector('.errrat').classList.remove('hideErr');
      document.querySelector('.errrat').innerHTML = "Rating should be from 1 to 5!";
  }
  else{
    // alert("Rating successful!")
    document.querySelector('.bid2').type = 'submit'
    // location.reload()
  }
}
}
// SHOW SIGN OUT MODAL
function logoutShow(){
  document.querySelector('.logoutC').classList.add('logoutS')
}
