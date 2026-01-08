
// PlantDocBot - Frontend JavaScript


// Configuration
const API_URL = 'http://127.0.0.1:5000';

// Global variables
let selectedImage = null;
let selectedImageCombined = null;


// Initialization


document.addEventListener('DOMContentLoaded', function() {
    console.log('PlantDocBot initialized');
    initializeTabs();
    initializeUploadAreas();
    initializeButtons();
});


// Tab Management


function initializeTabs() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;
            
            // Remove active class from all
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to selected
            tab.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
            
            // Hide results and errors when switching tabs
            hideResults();
            hideError();
        });
    });
}


// Upload Area Management


function initializeUploadAreas() {
    // Single image upload (Image tab)
    const uploadArea = document.getElementById('upload-area');
    const imageInput = document.getElementById('image-input');
    const previewImage = document.getElementById('preview-image');
    const uploadPlaceholder = uploadArea.querySelector('.upload-placeholder');
    
    uploadArea.addEventListener('click', () => imageInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('drop', (e) => handleDrop(e, imageInput, previewImage, uploadPlaceholder));
    imageInput.addEventListener('change', (e) => handleImageSelect(e, previewImage, uploadPlaceholder));
    
    // Combined upload (Both tab)
    const uploadAreaCombined = document.getElementById('upload-area-combined');
    const imageInputCombined = document.getElementById('image-input-combined');
    const previewImageCombined = document.getElementById('preview-image-combined');
    const uploadPlaceholderCombined = uploadAreaCombined.querySelector('.upload-placeholder');
    
    uploadAreaCombined.addEventListener('click', () => imageInputCombined.click());
    uploadAreaCombined.addEventListener('dragover', handleDragOver);
    uploadAreaCombined.addEventListener('drop', (e) => handleDrop(e, imageInputCombined, previewImageCombined, uploadPlaceholderCombined));
    imageInputCombined.addEventListener('change', (e) => handleImageSelect(e, previewImageCombined, uploadPlaceholderCombined));
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.style.borderColor = '#059669';
    e.currentTarget.style.background = '#d1fae5';
}

function handleDrop(e, input, previewImg, placeholder) {
    e.preventDefault();
    e.stopPropagation();
    
    e.currentTarget.style.borderColor = '';
    e.currentTarget.style.background = '';
    
    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type.startsWith('image/')) {
        input.files = files;
        const event = new Event('change');
        input.dispatchEvent(event);
    } else {
        showError('Please upload a valid image file (JPG, PNG, or JPEG)');
    }
}

function handleImageSelect(e, previewImg, placeholder) {
    const file = e.target.files[0];
    
    if (!file) return;
    
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file');
        return;
    }
    
    // Check file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('Image size should be less than 10MB');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(event) {
        previewImg.src = event.target.result;
        previewImg.style.display = 'block';
        placeholder.style.display = 'none';
    };
    reader.onerror = function() {
        showError('Error reading image file');
    };
    reader.readAsDataURL(file);
}


// Button Handlers


function initializeButtons() {
    document.getElementById('analyze-image-btn').addEventListener('click', analyzeImage);
    document.getElementById('analyze-text-btn').addEventListener('click', analyzeText);
    document.getElementById('analyze-combined-btn').addEventListener('click', analyzeCombined);
    document.getElementById('new-diagnosis-btn').addEventListener('click', resetForm);
}


// API Calls


async function analyzeImage() {
    const imageInput = document.getElementById('image-input');
    
    if (!imageInput.files || imageInput.files.length === 0) {
        showError('Please upload an image first');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', imageInput.files[0]);
    
    try {
        showLoading();
        
        const response = await fetch(`${API_URL}/predict/image`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to analyze image');
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('Error analyzing image: ' + error.message);
    } finally {
        hideLoading();
    }
}

async function analyzeText() {
    const symptomsInput = document.getElementById('symptoms-input');
    const text = symptomsInput.value.trim();
    
    if (!text) {
        showError('Please describe the symptoms you are observing');
        return;
    }
    
    if (text.length < 10) {
        showError('Please provide a more detailed description (at least 10 characters)');
        return;
    }
    
    try {
        showLoading();
        
        const response = await fetch(`${API_URL}/predict/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to analyze symptoms');
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('Error analyzing symptoms: ' + error.message);
    } finally {
        hideLoading();
    }
}

async function analyzeCombined() {
    const imageInput = document.getElementById('image-input-combined');
    const symptomsInput = document.getElementById('symptoms-input-combined');
    const text = symptomsInput.value.trim();
    
    if ((!imageInput.files || imageInput.files.length === 0) && !text) {
        showError('Please provide an image and/or symptom description');
        return;
    }
    
    const formData = new FormData();
    
    if (imageInput.files && imageInput.files.length > 0) {
        formData.append('image', imageInput.files[0]);
    }
    
    if (text) {
        formData.append('text', text);
    }
    
    try {
        showLoading();
        
        const response = await fetch(`${API_URL}/predict/combined`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to analyze inputs');
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('Error analyzing inputs: ' + error.message);
    } finally {
        hideLoading();
    }
}


// Display Functions


function displayResults(data) {
    // Get prediction data
    let prediction, information;
    
    if (data.final_disease) {
        // Combined prediction
        const imageConf = data.image_prediction ? data.image_prediction.confidence : 0;
        const textConf = data.text_prediction ? data.text_prediction.confidence : 0;
        
        prediction = {
            disease: data.final_disease,
            confidence: Math.max(imageConf, textConf)
        };
        information = data.information;
    } else {
        // Single prediction
        prediction = data.prediction;
        information = data.information;
    }
    
    // Display disease name
    const diseaseName = formatDiseaseName(prediction.disease);
    document.getElementById('disease-name').textContent = diseaseName;
    
    // Display confidence
    const confidencePercent = (prediction.confidence * 100).toFixed(1);
    document.getElementById('confidence-text').textContent = `Confidence: ${confidencePercent}%`;
    
    // Animate confidence bar
    setTimeout(() => {
        document.getElementById('confidence-fill').style.width = `${confidencePercent}%`;
    }, 100);
    
    // Display disease information
    if (information) {
        // Description
        document.getElementById('disease-description').textContent = 
            information.description || 'No description available';
        
        // Symptoms
        const symptomsList = document.getElementById('disease-symptoms');
        symptomsList.innerHTML = '';
        if (information.symptoms && information.symptoms.length > 0) {
            information.symptoms.forEach(symptom => {
                const li = document.createElement('li');
                li.textContent = symptom;
                symptomsList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'No specific symptoms available';
            symptomsList.appendChild(li);
        }
        
        // Treatment
        const treatmentList = document.getElementById('disease-treatment');
        treatmentList.innerHTML = '';
        if (information.treatment && information.treatment.length > 0) {
            information.treatment.forEach(treatment => {
                const li = document.createElement('li');
                li.textContent = treatment;
                treatmentList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'Consult agricultural experts for treatment recommendations';
            treatmentList.appendChild(li);
        }
        
        // Prevention
        const preventionList = document.getElementById('disease-prevention');
        preventionList.innerHTML = '';
        if (information.prevention && information.prevention.length > 0) {
            information.prevention.forEach(prevention => {
                const li = document.createElement('li');
                li.textContent = prevention;
                preventionList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'Practice good agricultural hygiene and monitor plants regularly';
            preventionList.appendChild(li);
        }
    }
    
    // Hide input section and show results
    document.querySelectorAll('.tab-content').forEach(tab => tab.style.display = 'none');
    document.getElementById('results-section').style.display = 'block';
    
    // Scroll to results
    document.getElementById('results-section').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
    });
}

function formatDiseaseName(name) {
    if (!name) return 'Unknown';
    
    return name
        .replace(/_/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
}


// UI State Management


function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.querySelectorAll('.tab-content').forEach(tab => tab.style.display = 'none');
    document.getElementById('results-section').style.display = 'none';
    document.getElementById('error-message').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function hideResults() {
    document.getElementById('results-section').style.display = 'none';
}

function showError(message) {
    hideLoading();
    document.getElementById('error-text').textContent = message;
    document.getElementById('error-message').style.display = 'flex';
    document.getElementById('error-message').scrollIntoView({ 
        behavior: 'smooth',
        block: 'center'
    });
}

function hideError() {
    document.getElementById('error-message').style.display = 'none';
}

function resetForm() {
    // Reset all inputs
    document.getElementById('image-input').value = '';
    document.getElementById('image-input-combined').value = '';
    document.getElementById('symptoms-input').value = '';
    document.getElementById('symptoms-input-combined').value = '';
    
    // Reset previews
    document.getElementById('preview-image').style.display = 'none';
    document.getElementById('preview-image-combined').style.display = 'none';
    
    // Show placeholders
    const uploadArea = document.getElementById('upload-area');
    const uploadPlaceholder = uploadArea.querySelector('.upload-placeholder');
    if (uploadPlaceholder) uploadPlaceholder.style.display = 'block';
    
    const uploadAreaCombined = document.getElementById('upload-area-combined');
    const uploadPlaceholderCombined = uploadAreaCombined.querySelector('.upload-placeholder');
    if (uploadPlaceholderCombined) uploadPlaceholderCombined.style.display = 'block';
    
    // Reset confidence bar
    document.getElementById('confidence-fill').style.width = '0%';
    
    // Hide results and errors
    hideResults();
    hideError();
    
    // Show first tab
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    tabs.forEach(t => t.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));
    tabs[0].classList.add('active');
    tabContents[0].classList.add('active');
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    selectedImage = null;
    selectedImageCombined = null;
}

//handling error

window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
});

//checking connection

async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        console.log('Backend status:', data);
        return true;
    } catch (error) {
        console.error('Backend connection failed:', error);
        showError('Cannot connect to backend server. Please make sure the server is running on port 5000.');
        return false;
    }
}

// Check connection on load
setTimeout(checkBackendConnection, 1000);