// Image preview functionality
document.addEventListener('DOMContentLoaded', function() {
  const imageInput = document.getElementById('{{ form.image.id_for_label }}');
  const imagePreview = document.getElementById('image-preview');
  const fileName = document.getElementById('file-name');
  
  imageInput.addEventListener('change', function() {
      if (this.files && this.files[0]) {
          const file = this.files[0];
          
          // Update file name display
          fileName.textContent = file.name;
          
          // Create image preview
          const reader = new FileReader();
          reader.onload = function(e) {
              imagePreview.innerHTML = '';
              const img = document.createElement('img');
              img.src = e.target.result;
              img.alt = 'Preview';
              img.className = 'preview-image';
              imagePreview.appendChild(img);
          }
          reader.readAsDataURL(file);
      } else {
          fileName.textContent = 'No file chosen';
          imagePreview.innerHTML = '<div class="no-preview">Image preview will appear here</div>';
      }
  });
});

function toggleMenu() {
    var navLinks = document.getElementById("navLinks");
    navLinks.classList.toggle("show");
}
