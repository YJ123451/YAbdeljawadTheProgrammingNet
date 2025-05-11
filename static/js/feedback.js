document.addEventListener('DOMContentLoaded', function() {
    // Character counter for comments
    const commentsTextarea = document.getElementById('comments');
    const charCount = document.getElementById('char-count');
    
    if (commentsTextarea && charCount) {
      commentsTextarea.addEventListener('input', function() {
        const currentLength = this.value.length;
        charCount.textContent = currentLength;
        
        // Add visual feedback when approaching the limit
        if (currentLength > 1800) {
          charCount.style.color = '#ff3333';
        } else if (currentLength > 1500) {
          charCount.style.color = '#ff9933';
        } else {
          charCount.style.color = ''; // Reset to default
        }
      });
    }
    
    // Star rating hover effect enhancement
    const starLabels = document.querySelectorAll('.star-rating label');
    
    if (starLabels.length > 0) {
      starLabels.forEach(label => {
        label.addEventListener('mouseover', function() {
          // Add temporary hover class to create a smoother effect
          this.classList.add('hover');
        });
        
        label.addEventListener('mouseout', function() {
          this.classList.remove('hover');
        });
      });
    }
    
    // Form validation
    const feedbackForm = document.getElementById('feedback-form');
    
    if (feedbackForm) {
      feedbackForm.addEventListener('submit', function(event) {
        let isValid = true;
        
        // Check if rating is selected
        const ratingInputs = document.querySelectorAll('input[name="rating"]');
        let ratingSelected = false;
        
        ratingInputs.forEach(input => {
          if (input.checked) {
            ratingSelected = true;
          }
        });
        
        if (!ratingSelected) {
          isValid = false;
          alert('Please select a rating');
        }
        
        // Check if category is selected
        const categorySelect = document.getElementById('category');
        if (categorySelect.value === "") {
          isValid = false;
          categorySelect.classList.add('error');
          alert('Please select a category');
        }
        
        // Check if comments are provided
        const commentsField = document.getElementById('comments');
        if (commentsField.value.trim() === "") {
          isValid = false;
          commentsField.classList.add('error');
          alert('Please provide your comments');
        }
        
        if (!isValid) {
          event.preventDefault();
        }
      });
      
      // Remove error class when user starts typing
      const formInputs = feedbackForm.querySelectorAll('input, select, textarea');
      formInputs.forEach(input => {
        input.addEventListener('input', function() {
          this.classList.remove('error');
        });
      });
    }
  });
  