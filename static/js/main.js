/**
 * CARCRAFT — Modern Luxury Automotive Dealership Suite
 * Vanilla JavaScript Core Engine
 */

document.addEventListener('DOMContentLoaded', () => {
    initNavbarScroll();
    initVideoHero();
    initWishlistToggles();
    initCartInteractions();
    initAddToCartForms();
    initAutoDismissAlerts();
});

/**
 * 1. Navbar Scroll Transition
 * Transparent on hero -> Dark graphite with backdrop blur when scrolled
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.cc-navbar');
    if (!navbar) return;

    // Check if the current page has a hero video
    const hasHero = document.querySelector('.cc-hero');
    if (!hasHero) {
        navbar.classList.add('solid');
        return;
    }

    const handleScroll = () => {
        if (window.scrollY > 40) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
}

/**
 * 2. Hero Video Error & Autoplay Guard
 * Ensures seamless HTML5 autoplay behavior and graceful handling
 */
function initVideoHero() {
    const video = document.querySelector('.hero-video');
    if (!video) return;

    video.play().catch(() => {
        // In case browser policy restricts immediate unmuted autoplay
        video.muted = true;
        video.play().catch(e => {
            console.log("[CarCraft] Video autoplay note:", e.message);
        });
    });
}

/**
 * 3. Dynamic Wishlist AJAX Toggle
 * Toggles vehicle or product wishlist and updates badge without reloading
 */
function initWishlistToggles() {
    document.querySelectorAll('.cc-wishlist-toggle').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const url = btn.getAttribute('data-url');
            if (!url) return;

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCsrfToken(),
                    }
                });

                if (response.status === 401 || response.redirected) {
                    window.location.href = '/accounts/login/?next=' + encodeURIComponent(window.location.pathname);
                    return;
                }

                const data = await response.json();
                if (data.success) {
                    if (data.added) {
                        btn.classList.add('active');
                        btn.querySelector('i').classList.remove('bi-heart');
                        btn.querySelector('i').classList.add('bi-heart-fill');
                    } else {
                        btn.classList.remove('active');
                        btn.querySelector('i').classList.remove('bi-heart-fill');
                        btn.querySelector('i').classList.add('bi-heart');
                        
                        // If on wishlist page, remove the card row
                        const wishlistCard = btn.closest('.cc-wishlist-item');
                        if (wishlistCard) {
                            wishlistCard.style.opacity = '0';
                            wishlistCard.style.transform = 'scale(0.95)';
                            setTimeout(() => wishlistCard.remove(), 300);
                        }
                    }

                    // Update navbar badge
                    const badge = document.querySelector('.cc-wishlist-badge');
                    if (badge) {
                        badge.textContent = data.wishlist_count;
                        badge.style.display = data.wishlist_count > 0 ? 'inline-block' : 'none';
                    }

                    showNotification(data.message || 'Wishlist updated');
                }
            } catch (err) {
                // Fallback to normal navigation if not logged in
                window.location.href = url;
            }
        });
    });
}

/**
 * 4. Cart Live Quantity AJAX
 */
function initCartInteractions() {
    document.querySelectorAll('.cc-cart-qty-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const form = btn.closest('form');
            if (!form) return;

            const url = form.getAttribute('action');
            const formData = new FormData(form);
            formData.set('action', btn.getAttribute('data-action'));

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCsrfToken(),
                    },
                    body: formData
                });

                if (response.ok) {
                    // Refresh cart for guaranteed sync
                    window.location.reload();
                }
            } catch (err) {
                form.submit();
            }
        });
    });
}

/**
 * 5. AJAX Add to Cart
 * Allows adding products to cart without leaving the showroom/catalog page
 */
function initAddToCartForms() {
    document.querySelectorAll('form[action*="/orders/cart/add/"]').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const url = form.getAttribute('action');
            const formData = new FormData(form);

            const submitBtn = form.querySelector('button[type="submit"]');
            const originalBtnHtml = submitBtn ? submitBtn.innerHTML : '';
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Adding...';
            }

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCsrfToken(),
                    },
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        // Update cart badge in navbar
                        const badge = document.querySelector('.cc-cart-badge');
                        if (badge) {
                            badge.textContent = data.cart_count;
                            badge.style.display = data.cart_count > 0 ? 'inline-block' : 'none';
                        }
                        showNotification(data.message || 'Item added to your cart.');
                    }
                } else {
                    form.submit();
                }
            } catch (err) {
                form.submit();
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnHtml;
                }
            }
        });
    });
}

/**
 * Helper to get Django CSRF Token
 */
function getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue || '';
}

/**
 * Toast Notification Banner
 */
function showNotification(message) {
    let toast = document.getElementById('cc-floating-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'cc-floating-toast';
        toast.className = 'position-fixed bottom-0 end-0 p-3';
        toast.style.zIndex = '9999';
        document.body.appendChild(toast);
    }

    toast.innerHTML = `
        <div class="toast align-items-center text-white bg-dark border-0 show" style="background-color: #161a22 !important; border: 1px solid #e85a19 !important; box-shadow: 0 10px 25px rgba(0,0,0,0.7);" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body d-flex align-items-center gap-2">
                    <i class="bi bi-info-circle-fill text-warning"></i>
                    <span>${message}</span>
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

    setTimeout(() => {
        if (toast) toast.innerHTML = '';
    }, 3500);
}

/**
 * Auto-dismiss alerts after 5 seconds
 */
function initAutoDismissAlerts() {
    setTimeout(() => {
        document.querySelectorAll('.alert.alert-dismissible').forEach(alert => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 400);
        });
    }, 5000);
}

/**
 * Indian Rupee (INR) Currency Formatter
 * Formats numbers into standard Indian localized currency strings (e.g. ₹52,00,000)
 */
const inrFormatter = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
});

function formatINR(amount) {
    return inrFormatter.format(amount);
}

