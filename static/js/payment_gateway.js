document.addEventListener('DOMContentLoaded', function() {
    const paymentMethodCards = document.querySelectorAll('.payment-method-card');
    let selectedMethod = null;
    let paymentCheckInterval = null;

    // Handle payment method selection
    paymentMethodCards.forEach(card => {
        card.addEventListener('click', function() {
            // Remove selected class from all cards
            paymentMethodCards.forEach(c => c.classList.remove('selected'));
            
            // Add selected class to clicked card
            this.classList.add('selected');
            
            // Store selected method
            selectedMethod = this.dataset.method;
            
            // Show payment processing UI
            showPaymentProcessing(selectedMethod);
        });
    });

    function showPaymentProcessing(method) {
        // Create processing modal
        const modal = document.createElement('div');
        modal.className = 'payment-processing-modal';
        modal.innerHTML = `
            <div class="processing-content">
                <div class="spinner-border text-primary mb-3" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <h5 class="text-white mb-3">Processing Payment</h5>
                <p class="text-white-50 mb-0">Please wait while we connect to ${getMethodName(method)}...</p>
            </div>
        `;
        document.body.appendChild(modal);

        // Get order ID from URL
        const orderId = window.location.pathname.split('/').filter(Boolean).pop();

        // Initiate payment
        initiatePayment(method, orderId);
    }

    function getMethodName(method) {
        const methods = {
            'mpesa': 'M-PESA',
            'tigopesa': 'Tigo Pesa',
            'airtel': 'Airtel Money',
            'halopesa': 'Halo Pesa'
        };
        return methods[method] || method;
    }

    function initiatePayment(method, orderId) {
        const formData = new FormData();
        formData.append('payment_method', method);

        fetch(`/initiate-payment/${orderId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            // Remove processing modal
            const modal = document.querySelector('.payment-processing-modal');
            if (modal) {
                modal.remove();
            }

            if (data.status === 'success') {
                if (method === 'mpesa') {
                    showMpesaPrompt(data.message);
                    // Start checking payment status
                    startPaymentStatusCheck(orderId);
                } else {
                    showSuccessMessage(data.message);
                }
            } else {
                showErrorMessage(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showErrorMessage('An error occurred while processing your payment.');
        });
    }

    function showMpesaPrompt(message) {
        const successMessage = document.createElement('div');
        successMessage.className = 'payment-success-message';
        successMessage.innerHTML = `
            <div class="success-content">
                <i class="fas fa-mobile-alt text-primary mb-3" style="font-size: 3rem;"></i>
                <h5 class="text-white mb-3">M-PESA Payment Initiated</h5>
                <p class="text-white-50 mb-0">${message}</p>
                <div class="mt-4">
                    <div class="spinner-border spinner-border-sm text-primary me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <span class="text-white-50">Waiting for payment confirmation...</span>
                </div>
            </div>
        `;
        document.body.appendChild(successMessage);
    }

    function startPaymentStatusCheck(orderId) {
        // Check payment status every 5 seconds
        paymentCheckInterval = setInterval(() => {
            checkPaymentStatus(orderId);
        }, 5000);
    }

    function checkPaymentStatus(orderId) {
        fetch(`/check-payment-status/${orderId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success' && data.order_status === 'approved') {
                    // Payment successful
                    clearInterval(paymentCheckInterval);
                    showSuccessMessage('Payment successful!');
                    setTimeout(() => {
                        window.location.href = '/order-confirmation/';
                    }, 2000);
                } else if (data.status === 'error') {
                    // Payment failed
                    clearInterval(paymentCheckInterval);
                    showErrorMessage(data.message);
                }
                // If status is pending, continue checking
            })
            .catch(error => {
                console.error('Error:', error);
                clearInterval(paymentCheckInterval);
                showErrorMessage('Error checking payment status.');
            });
    }

    function showSuccessMessage(message) {
        const successMessage = document.createElement('div');
        successMessage.className = 'payment-success-message';
        successMessage.innerHTML = `
            <div class="success-content">
                <i class="fas fa-check-circle text-success mb-3" style="font-size: 3rem;"></i>
                <h5 class="text-white mb-3">Payment Successful</h5>
                <p class="text-white-50 mb-0">${message}</p>
            </div>
        `;
        document.body.appendChild(successMessage);

        // Get order ID from URL
        const orderId = window.location.pathname.split('/').filter(Boolean).pop();

        setTimeout(() => {
            successMessage.remove();
            window.location.href = `/order-confirmation/${orderId}/`;
        }, 2000);
    }

    function showErrorMessage(message) {
        const errorMessage = document.createElement('div');
        errorMessage.className = 'payment-success-message';
        errorMessage.innerHTML = `
            <div class="success-content">
                <i class="fas fa-times-circle text-danger mb-3" style="font-size: 3rem;"></i>
                <h5 class="text-white mb-3">Payment Failed</h5>
                <p class="text-white-50 mb-0">${message}</p>
                <button class="btn btn-primary mt-3" onclick="window.location.reload()">
                    Try Again
                </button>
            </div>
        `;
        document.body.appendChild(errorMessage);
    }

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
});

// Add styles for payment processing modal
const style = document.createElement('style');
style.textContent = `
    .payment-processing-modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }

    .processing-content {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        backdrop-filter: blur(10px);
    }

    .payment-success-message {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }

    .success-content {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
`;
document.head.appendChild(style); 