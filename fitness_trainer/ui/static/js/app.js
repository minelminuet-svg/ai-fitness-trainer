/**
 * Main Application Logic for AI Fitness Trainer
 */

// Global state
let appState = {
    currentExercise: null,
    currentSession: null,
    isTraining: false,
    trainingStartTime: null,
    videoStream: null,
    selectedExerciseId: null,
};

// Initialize app on page load
document.addEventListener('DOMContentLoaded', initializeApp);

async function initializeApp() {
    console.log('Initializing AI Fitness Trainer...');
    
    try {
        // Check API health
        await checkAPIHealth();
        
        // Setup event listeners
        setupEventListeners();
        
        // Load initial data
        await loadExercises();
        
        console.log('App initialized successfully');
        showNotification('Welcome to AI Fitness Trainer!', 'success');
    } catch (error) {
        console.error('Failed to initialize app:', error);
        showNotification('Failed to initialize app. Please refresh the page.', 'error');
    }
}

/**
 * Check API health status
 */
async function checkAPIHealth() {
    const healthStatus = document.getElementById('healthStatus');
    
    try {
        const isHealthy = await apiClient.checkHealth();
        
        if (isHealthy) {
            healthStatus.textContent = '✓ Connected';
            healthStatus.style.color = '#10b981';
        } else {
            healthStatus.textContent = '✗ Offline';
            healthStatus.style.color = '#ef4444';
        }
    } catch (error) {
        healthStatus.textContent = '✗ Offline';
        healthStatus.style.color = '#ef4444';
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Navigation buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const viewName = e.target.dataset.view;
            switchView(viewName);
        });
    });
    
    // Filter changes
    document.getElementById('typeFilter').addEventListener('change', loadExercises);
    document.getElementById('difficultyFilter').addEventListener('change', loadExercises);
}

/**
 * Switch between views
 */
function switchView(viewName) {
    // Update active nav button
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.view === viewName) {
            btn.classList.add('active');
        }
    });
    
    // Update active view
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });
    
    const targetView = document.getElementById(`${viewName}View`);
    if (targetView) {
        targetView.classList.add('active');
    }
}

/**
 * Load exercises from API
 */
async function loadExercises() {
    try {
        const typeFilter = document.getElementById('typeFilter').value;
        const difficultyFilter = document.getElementById('difficultyFilter').value;
        
        const response = await apiClient.getAllExercises(typeFilter || null, difficultyFilter || null);
        
        if (response.success) {
            displayExercises(response.exercises);
        }
    } catch (error) {
        console.error('Failed to load exercises:', error);
        showNotification('Failed to load exercises', 'error');
    }
}

/**
 * Display exercises in grid
 */
function displayExercises(exercises) {
    const grid = document.getElementById('exercisesGrid');
    
    if (!exercises || exercises.length === 0) {
        grid.innerHTML = '<p class="placeholder">No exercises found</p>';
        return;
    }
    
    grid.innerHTML = exercises.map(exercise => formatExerciseCard(exercise)).join('');
}

/**
 * Select an exercise
 */
function selectExercise(exerciseId, exerciseName) {
    appState.selectedExerciseId = exerciseId;
    appState.currentExercise = exerciseName;
    
    // Update UI
    document.getElementById('currentExercise').textContent = exerciseName;
    
    // Load exercise details
    loadExerciseDetails(exerciseId);
    
    // Switch to training view
    switchView('training');
}

/**
 * Load exercise details
 */
async function loadExerciseDetails(exerciseId) {
    try {
        const response = await apiClient.getExerciseDetails(exerciseId);
        
        if (response.success) {
            const exercise = response.exercise;
            
            // Update description
            document.getElementById('exerciseDescription').textContent = exercise.description;
            
            // Update form feedback with tips
            const feedbackList = document.getElementById('feedbackList');
            feedbackList.innerHTML = exercise.tips
                .map(tip => `<div class="feedback-item tip">💡 ${tip}</div>`)
                .join('');
        }
    } catch (error) {
        console.error('Failed to load exercise details:', error);
    }
}

/**
 * Start training session
 */
async function startTraining() {
    if (!appState.selectedExerciseId) {
        showNotification('Please select an exercise first', 'warning');
        return;
    }
    
    try {
        const response = await apiClient.createSession(appState.selectedExerciseId);
        
        if (response.success) {
            appState.currentSession = response.session_id;
            appState.isTraining = true;
            appState.trainingStartTime = Date.now();
            
            // Update UI
            document.getElementById('startBtn').disabled = true;
            document.getElementById('pauseBtn').disabled = false;
            document.getElementById('endBtn').disabled = false;
            
            // Start video capture
            startVideoCapture();
            
            // Start training loop
            startTrainingLoop();
            
            showNotification('Training session started', 'success');
        }
    } catch (error) {
        console.error('Failed to start training:', error);
        showNotification('Failed to start training session', 'error');
    }
}

/**
 * Start video capture from webcam
 */
async function startVideoCapture() {
    try {
        const video = document.getElementById('videoFeed');
        const canvas = document.getElementById('canvas');
        
        // Request camera access
        appState.videoStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'user' },
            audio: false
        });
        
        video.srcObject = appState.videoStream;
        
        // Show video element (hide placeholder)
        document.querySelector('.video-placeholder').style.display = 'none';
        video.style.display = 'block';
        
    } catch (error) {
        console.error('Failed to access camera:', error);
        showNotification('Cannot access camera. Please check permissions.', 'error');
    }
}

/**
 * Training loop - process frames and update form feedback
 */
function startTrainingLoop() {
    if (!appState.isTraining) return;
    
    // Update duration
    const elapsed = Math.floor((Date.now() - appState.trainingStartTime) / 1000);
    document.getElementById('duration').textContent = formatTime(elapsed);
    
    // Simulate form score updates (in real implementation, would process poses)
    const formScore = 0.75 + Math.random() * 0.2; // Random between 0.75 and 0.95
    document.getElementById('formScore').textContent = formatPercentage(formScore);
    
    // Update form feedback
    updateFormFeedback(formScore);
    
    // Continue loop
    requestAnimationFrame(startTrainingLoop);
}

/**
 * Update form feedback based on score
 */
async function updateFormFeedback(formScore) {
    if (!appState.selectedExerciseId) return;
    
    try {
        const response = await apiClient.getFormFeedback(appState.selectedExerciseId, formScore);
        
        if (response.success) {
            const feedbackList = document.getElementById('feedbackList');
            feedbackList.innerHTML = response.feedback
                .map(item => `<div class="feedback-item ${item.priority}">
                    ${item.priority === 'critical' ? '⚠️' : item.priority === 'warning' ? '⚡' : '💡'} 
                    ${item.message}
                </div>`)
                .join('');
        }
    } catch (error) {
        // Silently fail feedback updates
    }
}

/**
 * Pause training session
 */
function pauseTraining() {
    appState.isTraining = false;
    document.getElementById('pauseBtn').textContent = 'Resume';
    document.getElementById('pauseBtn').onclick = resumeTraining;
}

/**
 * Resume training session
 */
function resumeTraining() {
    appState.isTraining = true;
    appState.trainingStartTime = Date.now() - (parseInt(document.getElementById('duration').textContent.split(':')[0]) * 60 + parseInt(document.getElementById('duration').textContent.split(':')[1])) * 1000;
    document.getElementById('pauseBtn').textContent = 'Pause';
    document.getElementById('pauseBtn').onclick = pauseTraining;
    startTrainingLoop();
}

/**
 * End training session
 */
async function endTraining() {
    if (!appState.currentSession) return;
    
    try {
        await apiClient.endSession(appState.currentSession);
        
        // Stop video
        if (appState.videoStream) {
            appState.videoStream.getTracks().forEach(track => track.stop());
        }
        
        // Reset UI
        document.getElementById('startBtn').disabled = false;
        document.getElementById('pauseBtn').disabled = true;
        document.getElementById('endBtn').disabled = true;
        document.getElementById('pauseBtn').textContent = 'Pause';
        document.getElementById('pauseBtn').onclick = pauseTraining;
        
        // Reset state
        appState.isTraining = false;
        appState.currentSession = null;
        
        // Reset video display
        const video = document.getElementById('videoFeed');
        video.style.display = 'none';
        document.querySelector('.video-placeholder').style.display = 'flex';
        
        showNotification('Training session completed!', 'success');
    } catch (error) {
        console.error('Failed to end training:', error);
        showNotification('Failed to end training session', 'error');
    }
}

/**
 * Update rep/set counter (mocked)
 */
function updateRepCount(reps, sets) {
    document.getElementById('repCount').textContent = reps;
    document.getElementById('setCount').textContent = sets;
}

// Expose functions to global scope for onclick handlers
window.switchView = switchView;
window.selectExercise = selectExercise;
window.startTraining = startTraining;
window.pauseTraining = pauseTraining;
window.resumeTraining = resumeTraining;
window.endTraining = endTraining;
window.showNotification = showNotification;
