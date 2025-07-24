// Debug function to check if elements exist
function debugElements() {
    const elements = {
        packageSelect: document.getElementById('packageSelect'),
        serviceSelect: document.getElementById('serviceSelect'),
        quantityInput: document.getElementById('quantity'),
        totalPriceSpan: document.getElementById('totalPrice'),
        serviceIdInput: document.getElementById('serviceId'),
        packageIdInput: document.getElementById('packageId'),
        toggleServiceDesc: document.getElementById('toggleServiceDesc'),
        serviceDescription: document.getElementById('serviceDescription'),
        descriptionText: document.getElementById('descriptionText')
    };

    console.log('Debug - Checking Elements:', elements);
    return elements;
}

// Initialize the form
function initializeForm() {
    console.log('Initializing form...');
    const elements = debugElements();
    
    if (!elements.packageSelect || !elements.serviceSelect || !elements.quantityInput || !elements.totalPriceSpan) {
        console.error('Required elements not found!');
        return;
    }

    let currentServicePrice = 0;

    // Package selection handler
    elements.packageSelect.addEventListener('change', function() {
        console.log('Package selection changed:', this.value);
        const selectedOption = this.options[this.selectedIndex];
        if (selectedOption.value) {
            console.log('Selected package:', {
                id: selectedOption.value,
                name: selectedOption.text,
                description: selectedOption.dataset.description
            });
            
            elements.packageDescriptionText.textContent = selectedOption.dataset.description;
            elements.packageDescription.classList.remove('d-none');
            elements.packageIdInput.value = selectedOption.value;
            
            // Fetch services for the selected package
            console.log('Fetching services for package:', selectedOption.value);
            fetch(`/api/package/${selectedOption.value}/services/`)
                .then(response => response.json())
                .then(data => {
                    console.log('Services data received:', data);
                    if (data.status === 'success') {
                        elements.serviceSelect.innerHTML = '<option value="" selected disabled>Select Service Type</option>';
                        data.services.forEach(service => {
                            console.log('Adding service:', service);
                            const option = document.createElement('option');
                            option.value = service.id;
                            option.textContent = service.name;
                            option.dataset.price = service.price;
                            option.dataset.description = service.description;
                            elements.serviceSelect.appendChild(option);
                        });
                        elements.serviceSelect.disabled = false;
                    }
                })
                .catch(error => console.error('Error fetching services:', error));
        } else {
            console.log('No package selected, resetting form');
            elements.packageDescription.classList.add('d-none');
            elements.serviceSelect.disabled = true;
            elements.serviceSelect.innerHTML = '<option value="" selected disabled>Select Service Type</option>';
            resetForm();
        }
    });

    // Service selection handler
    elements.serviceSelect.addEventListener('change', function() {
        console.log('Service selection changed:', this.value);
        const selectedOption = this.options[this.selectedIndex];
        if (selectedOption.value) {
            currentServicePrice = parseFloat(selectedOption.dataset.price);
            console.log('Selected service:', {
                id: selectedOption.value,
                name: selectedOption.text,
                price: currentServicePrice,
                description: selectedOption.dataset.description
            });
            
            elements.descriptionText.textContent = selectedOption.dataset.description;
            elements.toggleServiceDesc.classList.remove('d-none');
            elements.toggleServiceDesc.setAttribute('aria-expanded', 'false');
            elements.toggleServiceDesc.innerHTML = '<i class="fas fa-chevron-down me-1"></i> Show Service Description';
            elements.serviceDescription.classList.add('d-none');
            elements.serviceIdInput.value = selectedOption.value;
            updateTotalPrice();
            elements.submitOrderBtn.disabled = false;
        } else {
            console.log('No service selected, resetting form');
            resetForm();
        }
    });

    // Quantity input handlers
    elements.quantityInput.addEventListener('input', function() {
        console.log('Quantity input changed:', this.value);
        updateTotalPrice();
    });

    elements.quantityInput.addEventListener('change', function() {
        console.log('Quantity changed:', this.value);
        updateTotalPrice();
    });

    // Toggle service description
    elements.toggleServiceDesc.addEventListener('click', function() {
        const expanded = this.getAttribute('aria-expanded') === 'true';
        if (expanded) {
            elements.serviceDescription.classList.add('d-none');
            this.setAttribute('aria-expanded', 'false');
            this.innerHTML = '<i class="fas fa-chevron-down me-1"></i> Show Service Description';
        } else {
            elements.serviceDescription.classList.remove('d-none');
            this.setAttribute('aria-expanded', 'true');
            this.innerHTML = '<i class="fas fa-chevron-up me-1"></i> Hide Service Description';
        }
    });

    // Update total price
    function updateTotalPrice() {
        const quantity = parseInt(elements.quantityInput.value) || 0;
        console.log('Updating price:', {
            quantity: quantity,
            servicePrice: currentServicePrice,
            total: (currentServicePrice * quantity).toFixed(2)
        });
        const total = (currentServicePrice * quantity).toFixed(2);
        elements.totalPriceSpan.textContent = total;
    }

    // Reset form
    function resetForm() {
        currentServicePrice = 0;
        elements.quantityInput.value = '';
        elements.totalPriceSpan.textContent = '0.00';
        elements.submitOrderBtn.disabled = true;
        elements.serviceIdInput.value = '';
        elements.toggleServiceDesc.classList.add('d-none');
        elements.serviceDescription.classList.add('d-none');
    }

    // Form submission
    elements.orderForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!this.checkValidity()) {
            e.stopPropagation();
            this.classList.add('was-validated');
            return;
        }

        const formData = {
            service_id: elements.serviceIdInput.value,
            customer_name: elements.customerName.value,
            customer_email: elements.customerEmail.value,
            link: elements.link.value,
            quantity: parseInt(elements.quantityInput.value),
            total_price: parseFloat(elements.totalPriceSpan.textContent)
        };

        console.log('Submitting form data:', formData);

        fetch('/submit-order/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.redirect_url;
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while submitting the order. Please try again.');
        });
    });

    console.log('Form initialization complete');
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Starting initialization');
    initializeForm();
});

// Make debug function available globally
window.debugForm = debugElements; 