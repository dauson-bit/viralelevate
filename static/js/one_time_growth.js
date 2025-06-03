document.addEventListener('DOMContentLoaded', function() {
  const packageSelect = document.getElementById('packageSelect');
  const serviceSelect = document.getElementById('serviceSelect');
  const serviceDescription = document.getElementById('serviceDescription');
  const descriptionText = document.getElementById('descriptionText');
  const quantityInput = document.getElementById('quantity');
  const totalPriceSpan = document.getElementById('totalPrice');
  const submitOrderBtn = document.getElementById('submitOrder');
  const orderForm = document.getElementById('orderForm');
  const serviceIdInput = document.getElementById('serviceId');
  const packageIdInput = document.getElementById('packageId');
  const packageDescription = document.getElementById('packageDescription');
  const packageDescriptionText = document.getElementById('packageDescriptionText');
  const toggleServiceDesc = document.getElementById('toggleServiceDesc');
  
  let currentServicePrice = 0;

  // Enhanced package description display
  packageSelect.addEventListener('change', function() {
      const selectedOption = this.options[this.selectedIndex];
      if (selectedOption.value) {
          const description = selectedOption.dataset.description;
          if (description) {
              const formattedDescription = formatPackageDescription(description);
              packageDescriptionText.innerHTML = formattedDescription;
              packageDescription.classList.remove('d-none');
          } else {
              packageDescription.classList.add('d-none');
          }
          
          fetchServices(selectedOption.value);
      } else {
          resetForm();
          packageDescription.classList.add('d-none');
      }
  });

  function formatPackageDescription(description) {
      const sections = description.split('\n\n');
      let formattedHtml = '';

      sections.forEach(section => {
          if (section.trim()) {
              if (section.includes(':')) {
                  const [title, content] = section.split(':');
                  formattedHtml += `
                      <div class="mb-3">
                          <h6 class="text-primary mb-2">${title.trim()}</h6>
                          <div class="ps-3">
                              ${formatContent(content.trim())}
                          </div>
                      </div>
                  `;
              } else {
                  formattedHtml += `<p class="mb-2">${section.trim()}</p>`;
              }
          }
      });

      return formattedHtml;
  }

  function formatContent(content) {
      const lines = content.split('\n');
      if (lines.length > 1) {
          return `<ul class="list-unstyled mb-0">
              ${lines.map(line => `<li class="mb-1"><i class="fas fa-chevron-right text-primary me-2"></i>${line.trim()}</li>`).join('')}
          </ul>`;
      }
      return `<p class="mb-0">${content}</p>`;
  }

  function fetchServices(packageId) {
      serviceSelect.disabled = true;
      serviceSelect.innerHTML = '<option value="" selected disabled>Loading services...</option>';
      
      fetch(`/api/package/${packageId}/services/`)
          .then(response => {
              if (!response.ok) {
                  throw new Error('Network response was not ok');
              }
              return response.json();
          })
          .then(data => {
              if (data.status === 'success' && data.services.length > 0) {
                  serviceSelect.innerHTML = '<option value="" selected disabled>Choose a service</option>';
                  data.services.forEach(service => {
                      serviceSelect.innerHTML += `
                          <option value="${service.id}" 
                                  data-price="${service.price}"
                                  data-description="${service.description}">
                              ${service.name} - $${service.price}/${service.unit}
                          </option>
                      `;
                  });
                  serviceSelect.disabled = false;
                  packageIdInput.value = packageId;
              } else {
                  serviceSelect.innerHTML = '<option value="" selected disabled>No services available</option>';
                  serviceSelect.disabled = true;
              }
              resetForm();
          })
          .catch(error => {
              console.error('Error:', error);
              serviceSelect.innerHTML = '<option value="" selected disabled>Error loading services</option>';
              serviceSelect.disabled = true;
              resetForm();
          });
  }

  // Handle service selection
  serviceSelect.addEventListener('change', function() {
      const selectedOption = this.options[this.selectedIndex];
      if (selectedOption.value) {
          currentServicePrice = parseFloat(selectedOption.dataset.price);
          descriptionText.textContent = selectedOption.dataset.description;
          toggleServiceDesc.classList.remove('d-none');
          toggleServiceDesc.setAttribute('aria-expanded', 'false');
          toggleServiceDesc.innerHTML = '<i class="fas fa-chevron-down me-1"></i> Show Service Description';
          serviceDescription.classList.add('d-none');
          serviceIdInput.value = selectedOption.value;
          updateTotalPrice();
          submitOrderBtn.disabled = false;
      } else {
          resetForm();
      }
  });

  // Update total price when quantity changes
  quantityInput.addEventListener('input', updateTotalPrice);

  function updateTotalPrice() {
      const quantity = parseInt(quantityInput.value) || 0;
      console.log('Updating price:', {
          quantity: quantity,
          servicePrice: currentServicePrice,
          total: (currentServicePrice * quantity)
      });
      const total = (currentServicePrice * quantity).toFixed(2);
      totalPriceSpan.textContent = total;
  }

  function resetForm() {
      serviceDescription.classList.add('d-none');
      descriptionText.textContent = '';
      quantityInput.value = '';
      totalPriceSpan.textContent = '0.00';
      submitOrderBtn.disabled = true;
      serviceIdInput.value = '';
      currentServicePrice = 0;
  }

  // Toggle service description
  toggleServiceDesc.addEventListener('click', function() {
      const expanded = this.getAttribute('aria-expanded') === 'true';
      if (expanded) {
          serviceDescription.classList.add('d-none');
          this.setAttribute('aria-expanded', 'false');
          this.innerHTML = '<i class="fas fa-chevron-down me-1"></i> Show Service Description';
      } else {
          serviceDescription.classList.remove('d-none');
          this.setAttribute('aria-expanded', 'true');
          this.innerHTML = '<i class="fas fa-chevron-up me-1"></i> Hide Service Description';
      }
  });

  // Form submission
  orderForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      if (!this.checkValidity()) {
          e.stopPropagation();
          this.classList.add('was-validated');
          return;
      }

      const formData = {
          service_id: serviceIdInput.value,
          package_id: packageIdInput.value,
          customer_name: document.getElementById('customerName').value,
          customer_email: document.getElementById('customerEmail').value,
          customer_phone: document.getElementById('customerPhone').value,
          link: document.getElementById('link').value,
          quantity: parseInt(quantityInput.value),
          total_price: parseFloat(totalPriceSpan.textContent)
      };

      try {
          const response = await fetch('/submit-order/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': getCookie('csrftoken')
              },
              body: JSON.stringify(formData)
          });

          const data = await response.json();
          
          if (data.status === 'success') {
              window.location.href = data.redirect_url;
          } else {
              alert('Error submitting order: ' + data.message);
          }
      } catch (error) {
          console.error('Error:', error);
          alert('Error submitting order. Please try again.');
      }
  });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
