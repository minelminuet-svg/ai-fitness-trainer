/**
 * API Client for AI Fitness Trainer
 * Handles communication with the Flask backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

class APIClient {
    constructor(baseURL = API_BASE_URL) {
        this.baseURL = baseURL;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
        };
    }

    /**
     * Make API request
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                ...this.defaultHeaders,
                ...options.headers,
            },
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'API request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Exercise Endpoints
     */
    
    getAllExercises(type = null, difficulty = null) {
        let endpoint = '/exercises';
        const params = new URLSearchParams();
        
        if (type) params.append('type', type);
        if (difficulty) params.append('difficulty', difficulty);
        
        if (params.toString()) {
            endpoint += '?' + params.toString();
        }
        
        return this.request(endpoint);
    }

    getExerciseDetails(exerciseId) {
        return this.request(`/exercises/${exerciseId}`);
    }

    getExerciseTypes() {
        return this.request('/exercises/types');
    }

    getDifficultyLevels() {
        return this.request('/exercises/difficulties');
    }

    /**
     * Session Endpoints
     */
    
    createSession(exerciseId) {
        return this.request('/sessions', {
            method: 'POST',
            body: JSON.stringify({
                exercise_id: exerciseId,
            }),
        });
    }

    getSession(sessionId) {
        return this.request(`/sessions/${sessionId}`);
    }

    updateSession(sessionId, data) {
        return this.request(`/sessions/${sessionId}/update`, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    endSession(sessionId) {
        return this.request(`/sessions/${sessionId}/end`, {
            method: 'POST',
        });
    }

    /**
     * Analysis Endpoints
     */
    
    validatePose(exerciseId, landmarks, targetPosition) {
        return this.request('/analysis/validate', {
            method: 'POST',
            body: JSON.stringify({
                exercise_id: exerciseId,
                landmarks: landmarks,
                target_position: targetPosition,
            }),
        });
    }

    getFormFeedback(exerciseId, formScore) {
        return this.request('/analysis/feedback', {
            method: 'POST',
            body: JSON.stringify({
                exercise_id: exerciseId,
                form_score: formScore,
            }),
        });
    }

    analyzeJointAngles(landmarks) {
        return this.request('/analysis/jointangles', {
            method: 'POST',
            body: JSON.stringify({
                landmarks: landmarks,
            }),
        });
    }

    analyzePosture(landmarks) {
        return this.request('/analysis/posture', {
            method: 'POST',
            body: JSON.stringify({
                landmarks: landmarks,
            }),
        });
    }

    /**
     * Health Check
     */
    
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseURL.replace('/api', '')}/health`);
            return response.ok;
        } catch (error) {
            return false;
        }
    }
}

// Create global API client instance
const apiClient = new APIClient();
