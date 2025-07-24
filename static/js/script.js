// Counter Animation
document.addEventListener("DOMContentLoaded", function() {
    const counters = document.querySelectorAll('.counter');
    const speed = 200;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                let count = 0;
                const updateCount = () => {
                    const increment = target / speed;
                    if (count < target) {
                        count += increment;
                        counter.innerText = Math.ceil(count).toLocaleString();
                        setTimeout(updateCount, 1);
                    } else {
                        counter.innerText = target.toLocaleString();
                    }
                };
                updateCount();
                observer.unobserve(counter);
            }
        });
    }, {threshold: 0.5});
    
    counters.forEach(counter => {
        observer.observe(counter);
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Support Form Handler
    const submitSupportBtn = document.getElementById('submitSupportBtn');
    if (submitSupportBtn) {
        submitSupportBtn.addEventListener('click', function(e) {
            e.preventDefault();

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const data = {
                name: document.getElementById('supportName').value,
                email: document.getElementById('supportEmail').value,
                issue: document.getElementById('supportIssue').selectedOptions[0].text,
                message: document.getElementById('supportMessage').value,
            };

            fetch("{% url 'submit_payment_support' %}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                },
                body: new URLSearchParams(data),
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    alert("Your support request has been submitted!");
                    document.getElementById("paymentSupportForm").reset();
                    var modal = bootstrap.Modal.getInstance(document.getElementById('paymentSupportModal'));
                    modal.hide();
                } else {
                    alert("Error submitting the request. Please check your inputs.");
                }
            });
        });
    }
});

