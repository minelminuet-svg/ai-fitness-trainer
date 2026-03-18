/**
 * Utility Functions for AI Fitness Trainer
 */

/**
 * Format time in seconds to MM:SS format
 */
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Format number as percentage
 */
function formatPercentage(value) {
    return `${Math.round(value * 100)}%`;
}

/**
 * Get color based on score
 */
function getScoreColor(score) {
    if (score >= 0.9) return '#10b981'; // green
    if (score >= 0.7) return '#f59e0b'; // amber
    return '#ef4444'; // red
}

/**
 * Show notification
 */
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles if not already defined
    if (!document.querySelector('style[data-notifications]')) {
        const style = document.createElement('style');
        style.setAttribute('data-notifications', '');
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                animation: slideIn 0.3s ease;
                z-index: 1000;
                max-width: 300px;
            }
            
            .notification-info {
                background: #dbeafe;
                color: #1e40af;
            }
            
            .notification-success {
                background: #dcfce7;
                color: #166534;
            }
            
            .notification-warning {
                background: #fef3c7;
                color: #92400e;
            }
            
            .notification-error {
                background: #fee2e2;
                color: #991b1b;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Local Storage helpers
 */
const storage = {
    get: (key) => {
        const item = localStorage.getItem(key);
        try {
            return item ? JSON.parse(item) : null;
        } catch {
            return item;
        }
    },
    
    set: (key, value) => {
        localStorage.setItem(key, JSON.stringify(value));
    },
    
    remove: (key) => {
        localStorage.removeItem(key);
    },
    
    clear: () => {
        localStorage.clear();
    }
};

/**
 * Format exercise data for display
 */
function formatExerciseCard(exercise) {
    const difficultyColors = {
        'beginner': '#10b981',
        'intermediate': '#f59e0b',
        'advanced': '#ef4444'
    };
    
    const targetMuscleTags = exercise.target_muscles
        ? exercise.target_muscles.map(muscle => `<span class="muscle-tag">${muscle}</span>`).join('')
        : '';
    
    return `
        <div class="exercise-card" onclick="selectExercise('${exercise.id}', '${exercise.name}')">
            <div class="exercise-header">
                <h3>${exercise.name}</h3>
                <div class="exercise-tags">
                    <span class="tag">${exercise.type}</span>
                    <span class="tag difficulty-${exercise.difficulty}">${exercise.difficulty}</span>
                </div>
            </div>
            <p class="exercise-description">${exercise.description}</p>
            <div class="exercise-targets">
                <span>💪 Target:</span>
                <span>${exercise.target_muscles ? exercise.target_muscles.join(', ') : 'N/A'}</span>
            </div>
            <div class="exercise-targets">
                <span>🔄 Reps:</span>
                <span>${exercise.repetitions || 10} x ${exercise.sets || 3}</span>
            </div>
            <button class="exercise-button">Start Exercise</button>
        </div>
    `;
}

/**
 * Parse query parameters from URL
 */
function getQueryParams() {
    const params = {};
    const searchParams = new URLSearchParams(window.location.search);
    
    for (const [key, value] of searchParams.entries()) {
        params[key] = value;
    }
    
    return params;
}

/**
 * Generate unique ID
 */
function generateId() {
    return `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Clamp value between min and max
 */
function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
}

/**
 * Calculate average of array
 */
function average(arr) {
    return arr.length > 0 ? arr.reduce((a, b) => a + b) / arr.length : 0;
}

/**
 * Create exercise progress visualization
 */
function createProgressBar(current, target, width = 100) {
    const percentage = (current / target) * 100;
    const color = getScoreColor(percentage / 100);
    
    return `
        <div style="width: ${width}px; height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden;">
            <div style="width: ${percentage}%; height: 100%; background: ${color}; transition: width 0.3s ease;"></div>
        </div>
    `;
}

/**
 * Sleep utility for async operations
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Deep clone object
 */
function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

/**
 * Check if element is in viewport
 */
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}
