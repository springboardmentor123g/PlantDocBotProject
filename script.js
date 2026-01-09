// Backend server URL
const SERVER_URL = 'http://localhost:8000';

// State management
let selectedImage = null;
let currentChatId = null;
let isLoading = false;

// Initialize app
document.addEventListener('DOMContentLoaded', initializeApp);

function initializeApp() {
    console.log('🚀 App initialized at:', new Date().toLocaleTimeString());
    loadChatHistory();
    setupEventListeners();
    checkServerConnection();
}

// Setup all event listeners
function setupEventListeners() {
    const menuToggle = document.getElementById('menuToggle');
    const newChatBtn = document.getElementById('newChatBtn');
    const sendBtn = document.getElementById('sendBtn');
    const textInput = document.getElementById('textInput');
    const imageInput = document.getElementById('imageInput');
    const removeImgBtn = document.getElementById('removeImgBtn');
    const clearChatBtn = document.getElementById('clearChatBtn');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', toggleSidebar);
    }
    
    if (newChatBtn) {
        newChatBtn.addEventListener('click', startNewChat);
    }
    
    if (sendBtn) {
        sendBtn.addEventListener('click', handleSendMessage);
    }
    
    if (textInput) {
        textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
            }
        });
        
        textInput.addEventListener('input', updateCharCount);
    }
    
    if (imageInput) {
        imageInput.addEventListener('change', handleImageSelect);
    }
    
    if (removeImgBtn) {
        removeImgBtn.addEventListener('click', clearImage);
    }
    
    if (clearChatBtn) {
        clearChatBtn.addEventListener('click', confirmClearChat);
    }
}

// Check server connection
async function checkServerConnection() {
    try {
        const response = await fetch(`${SERVER_URL}/data`, {
            method: 'GET',
            signal: AbortSignal.timeout(10000)
        });
        
        if (!response.ok) {
            showToast('⚠️ Server connection issue', 'error');
        }
    } catch (err) {
        showToast('❌ Cannot connect to server. Please start the backend.', 'error');
        console.error('Server connection failed:', err);
    }
}

// Sidebar toggle
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('hidden');
    }
}

// Start new chat
function startNewChat() {
    currentChatId = null;
    
    const chatBody = document.getElementById('chatBody');
    if (chatBody) {
        chatBody.innerHTML = `
            <div class="welcome-screen">
                <div class="welcome-icon">🌿</div>
                <h1 class="welcome-title">Welcome to Plant Doctor Bot</h1>
                <p class="welcome-subtitle">Upload a plant image for instant disease detection!</p>
                <div class="welcome-features">
                    <div class="feature-card">
                        <span class="feature-icon">💬</span>
                        <span>Ask questions</span>
                    </div>
                    <div class="feature-card">
                        <span class="feature-icon">📸</span>
                        <span>Upload images</span>
                    </div>
                    <div class="feature-card">
                        <span class="feature-icon">🔬</span>
                        <span>Get AI diagnosis</span>
                    </div>
                </div>
            </div>
        `;
    }
    
    clearImage();
    updateClearButton();
    
    // Update sidebar
    document.querySelectorAll('.history-item').forEach(item => {
        item.classList.remove('active');
    });
    
    showToast('New chat started', 'success');
}

// Load chat history
async function loadChatHistory() {
    const historyContainer = document.getElementById('chatHistory');
    if (!historyContainer) return;
    
    try {
        const response = await fetch(`${SERVER_URL}/data`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        historyContainer.innerHTML = '';

        const chatsArray = Object.values(data.chats || {});
        
        if (chatsArray.length > 0) {
            chatsArray.sort((a, b) => {
                const dateA = new Date(a.updated_at || a.created_at);
                const dateB = new Date(b.updated_at || b.created_at);
                return dateB - dateA;
            });
            
            chatsArray.forEach((chat) => {
                const historyItem = createHistoryItem(chat);
                historyContainer.appendChild(historyItem);
            });
        } else {
            historyContainer.innerHTML = `
                <div style="padding: 20px; color: var(--text-secondary); font-size: 14px; text-align: center;">
                    No chat history yet<br>
                    <span style="font-size: 12px; opacity: 0.7;">Start diagnosing plants!</span>
                </div>
            `;
        }
    } catch (err) {
        console.error('Failed to load chat history:', err);
        historyContainer.innerHTML = `
            <div style="padding: 20px; color: var(--danger); font-size: 13px; text-align: center;">
                ⚠️ Unable to connect to server<br>
                <span style="font-size: 11px;">Make sure the backend is running</span>
            </div>
        `;
    }
}

// Create history item element
function createHistoryItem(chat) {
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    if (chat.id === currentChatId) {
        historyItem.classList.add('active');
    }
    
    const previewText = chat.title || 'Chat';
    const date = new Date(chat.updated_at || chat.created_at);
    const formattedDate = formatDate(date);
    
    historyItem.innerHTML = `
        <div class="history-item-content">
            <div class="history-item-text">${escapeHtml(previewText)}</div>
            <div class="history-date">${formattedDate}</div>
        </div>
        <button class="delete-chat-btn" title="Delete chat" data-chat-id="${chat.id}">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
        </button>
    `;
    
    // Load chat on click
    historyItem.addEventListener('click', (e) => {
        if (!e.target.closest('.delete-chat-btn')) {
            if (chat.id === currentChatId) {
                console.log('⚠️ Already viewing this chat');
                return;
            }
            loadChat(chat.id);
        }
    });
    
    // Delete chat
    const deleteBtn = historyItem.querySelector('.delete-chat-btn');
    deleteBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        confirmDeleteChat(chat.id);
    });
    
    return historyItem;
}

// Format date helper
function formatDate(date) {
    const now = new Date();
    const diff = now - date;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (seconds < 60) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;
    
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Load specific chat
async function loadChat(chatId) {
    try {
        const response = await fetch(`${SERVER_URL}/chat/${chatId}`);
        
        if (!response.ok) {
            throw new Error(`Failed to load chat: ${response.status}`);
        }
        
        const chat = await response.json();
        currentChatId = chatId;
        
        const chatBody = document.getElementById('chatBody');
        if (!chatBody) return;
        
        chatBody.innerHTML = '';
        
        chat.messages.forEach(msg => {
            if (msg.query_text) {
                addMessageToDOM(msg.query_text, 'user');
            }
            
            if (msg.image_token) {
                addMessageToDOM('📷 Image uploaded', 'user');
            }
            
            // Display disease prediction card
            if (msg.disease_prediction) {
                addDiseasePredictionCard(msg.disease_prediction);
            }
            
            // Display formatted text if no prediction
            if (msg.response_text && !msg.disease_prediction) {
                addFormattedBotMessage(msg.response_text);
            }
            
            // Display image thumbnail
            if (msg.bw_image_url) {
                addImageThumbnail(msg.bw_image_url);
            }
        });
        
        updateClearButton();
        
        document.querySelectorAll('.history-item').forEach(item => {
            item.classList.remove('active');
        });
        
        const activeItem = document.querySelector(`[data-chat-id="${chatId}"]`)?.closest('.history-item');
        if (activeItem) {
            activeItem.classList.add('active');
        }
        
    } catch (err) {
        console.error('Failed to load chat:', err);
        showToast('Failed to load chat', 'error');
    }
}

// Confirm delete chat
function confirmDeleteChat(chatId) {
    if (confirm('Are you sure you want to delete this chat?')) {
        deleteChat(chatId);
    }
}

// Delete chat
async function deleteChat(chatId) {
    try {
        const response = await fetch(`${SERVER_URL}/chat/${chatId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            if (chatId === currentChatId) {
                startNewChat();
            }
            loadChatHistory();
            showToast('Chat deleted', 'success');
        } else {
            throw new Error('Failed to delete chat');
        }
    } catch (err) {
        console.error('Failed to delete chat:', err);
        showToast('Failed to delete chat', 'error');
    }
}

// Confirm clear chat
function confirmClearChat() {
    if (currentChatId && confirm('Clear current chat? This cannot be undone.')) {
        deleteChat(currentChatId);
    }
}

// Handle image selection
function handleImageSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/bmp'];
    if (!validTypes.includes(file.type)) {
        showToast('Please select a valid image file', 'error');
        return;
    }
    
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
        showToast('Image too large (max 5MB)', 'error');
        return;
    }
    
    selectedImage = file;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        const preview = document.getElementById('imagePreview');
        const img = document.getElementById('previewImg');
        const name = document.getElementById('imageName');
        
        if (preview && img && name) {
            img.src = e.target.result;
            name.textContent = file.name;
            preview.style.display = 'flex';
        }
    };
    reader.readAsDataURL(file);
    
    showToast('Image selected', 'success');
}

// Clear selected image
function clearImage() {
    selectedImage = null;
    const imageInput = document.getElementById('imageInput');
    const preview = document.getElementById('imagePreview');
    
    if (imageInput) imageInput.value = '';
    if (preview) preview.style.display = 'none';
}

// Update character count
function updateCharCount() {
    const textInput = document.getElementById('textInput');
    const charCount = document.getElementById('charCount');
    
    if (textInput && charCount) {
        const length = textInput.value.length;
        charCount.textContent = `${length}/500`;
        
        if (length > 450) {
            charCount.style.color = 'var(--danger)';
        } else {
            charCount.style.color = 'var(--text-tertiary)';
        }
    }
}

// Update clear button visibility
function updateClearButton() {
    const clearBtn = document.getElementById('clearChatBtn');
    if (clearBtn) {
        clearBtn.style.display = currentChatId ? 'flex' : 'none';
    }
}

// Main send message function
async function handleSendMessage() {
    if (isLoading) return;

    const textInput = document.getElementById('textInput');
    const text = textInput ? textInput.value.trim() : '';
    const image = selectedImage;

    if (!text && !image) {
        showToast('Please enter text or upload an image', 'error');
        return;
    }

    console.log('📤 Sending message. Current chat:', currentChatId);

    // Remove welcome screen
    const welcomeScreen = document.querySelector('.welcome-screen');
    if (welcomeScreen) {
        welcomeScreen.remove();
    }

    // Display user messages
    if (text) {
        addMessageToDOM(text, 'user');
    }
    if (image) {
        addMessageToDOM('📷 Image uploaded: ' + image.name, 'user');
    }

    // Clear input
    if (textInput) {
        textInput.value = '';
        updateCharCount();
    }

    // Prepare form data
    const formData = new FormData();
    formData.append('text', text);
    if (image) {
        formData.append('image', image);
    }

    // Show loading
    isLoading = true;
    const loadingId = addLoadingMessage();
    updateSendButton(true);

    try {
        // Build URL with chat_id if it exists
        let url = `${SERVER_URL}/submit?q=${encodeURIComponent(text)}&img=${image ? encodeURIComponent(image.name) : ''}`;
        
        if (currentChatId) {
            url += `&chat_id=${currentChatId}`;
            console.log('✅ Continuing chat:', currentChatId);
        } else {
            console.log('🆕 Starting new chat');
        }

        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        console.log('📥 Response received:', data);

        // Save the chat_id
        if (data.chat_id) {
            currentChatId = data.chat_id;
            updateClearButton();
            console.log('💾 Saved currentChatId:', currentChatId);
        }

        // Remove loading
        removeMessage(loadingId);

        // Display bot response
        const message = data.message;

        // **KEY CHANGE**: Display disease prediction card prominently
        if (message?.disease_prediction && message.disease_prediction.success) {
            addDiseasePredictionCard(message.disease_prediction);
        } else if (message?.response_text) {
            // Fallback to text if no prediction
            addFormattedBotMessage(message.response_text);
        }

        // Display uploaded image as thumbnail (optional)
        if (message?.bw_image_url) {
            addImageThumbnail(message.bw_image_url);
        }

        // Clear image AFTER success
        clearImage();

        // Silently refresh sidebar
        loadChatHistory();

        showToast('Analysis complete!', 'success');

    } catch (err) {
        removeMessage(loadingId);
        console.error('Request failed:', err);
        addMessageToDOM('❌ Error: ' + err.message, 'bot');

        if (err.message.includes('Failed to fetch')) {
            showToast('Cannot connect to server', 'error');
        } else {
            showToast('Failed to send message', 'error');
        }
    } finally {
        isLoading = false;
        updateSendButton(false);
    }
}

// **NEW FUNCTION**: Add disease prediction card
// **IMPROVED FUNCTION**: Add disease prediction card
function addDiseasePredictionCard(prediction) {
    const chatBody = document.getElementById('chatBody');
    if (!chatBody) return;
    
    // Handle text-only queries (no image uploaded)
    if (prediction.text_only) {
        const div = document.createElement('div');
        div.className = 'message bot text-response';
        div.innerHTML = `
            <div style="padding: 16px;">
                <div style="font-size: 16px; font-weight: 600; color: var(--accent-blue); margin-bottom: 12px;">
                    📸 Image Required for Analysis
                </div>
                <div style="font-size: 14px; line-height: 1.7; color: var(--text-secondary);">
                    ${prediction.treatment || 'Please upload an image of your plant for accurate disease detection.'}
                </div>
            </div>
        `;
        chatBody.appendChild(div);
        scrollToBottom();
        return;
    }
    
    const isHealthy = prediction.is_healthy || false;
    const plant = prediction.plant || 'Unknown';
    const disease = prediction.disease || 'Unknown';
    const confidence = prediction.confidence || 'N/A';
    const treatment = prediction.treatment || 'No treatment information available';
    
    const div = document.createElement('div');
    div.className = 'message bot disease-card';
    
    const statusColor = isHealthy ? '#10b981' : '#ef4444';
    const statusIcon = isHealthy ? '✅' : '⚠️';
    const statusText = isHealthy ? 'Healthy Plant' : 'Disease Detected';
    const statusBg = isHealthy ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)';
    
    div.innerHTML = `
        <div style="max-width: 600px;">
            <!-- Status Header -->
            <div style="background: ${statusBg}; border-left: 4px solid ${statusColor}; padding: 16px; border-radius: 12px 12px 0 0; margin-bottom: 2px;">
                <div style="font-size: 20px; font-weight: 700; color: ${statusColor}; display: flex; align-items: center; gap: 8px;">
                    <span>${statusIcon}</span>
                    <span>${statusText}</span>
                </div>
            </div>
            
            <!-- Prediction Details -->
            <div style="background: var(--bg-tertiary); padding: 20px; margin-bottom: 2px;">
                <div style="display: grid; gap: 16px;">
                    <!-- Plant Type -->
                    <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--bg-secondary); border-radius: 10px;">
                        <span style="font-size: 28px;">🌿</span>
                        <div style="flex: 1;">
                            <div style="font-size: 12px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Plant Type</div>
                            <div style="font-size: 18px; font-weight: 700; color: var(--accent-primary);">${plant}</div>
                        </div>
                    </div>
                    
                    <!-- Disease/Status -->
                    <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--bg-secondary); border-radius: 10px;">
                        <span style="font-size: 28px;">${isHealthy ? '✨' : '🦠'}</span>
                        <div style="flex: 1;">
                            <div style="font-size: 12px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">${isHealthy ? 'Status' : 'Diagnosis'}</div>
                            <div style="font-size: 18px; font-weight: 700; color: ${statusColor};">${disease}</div>
                        </div>
                    </div>
                    
                    <!-- Confidence -->
                    <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--bg-secondary); border-radius: 10px;">
                        <span style="font-size: 28px;">📊</span>
                        <div style="flex: 1;">
                            <div style="font-size: 12px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Confidence Level</div>
                            <div style="font-size: 18px; font-weight: 700; color: var(--accent-blue);">${confidence}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Treatment Section -->
            <div style="background: var(--bg-secondary); padding: 20px; border-radius: 0 0 12px 12px; border-top: 1px solid var(--border-color);">
                <div style="font-size: 16px; font-weight: 700; color: var(--text-primary); margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 24px;">💊</span>
                    <span>${isHealthy ? 'Care Recommendations' : 'Treatment Plan'}</span>
                </div>
                <div style="font-size: 14px; line-height: 1.8; color: var(--text-secondary); white-space: pre-line;">${treatment}</div>
            </div>
        </div>
    `;
    
    // Add alternative predictions if available
    if (prediction.top_predictions && prediction.top_predictions.length > 1) {
        const altSection = document.createElement('div');
        altSection.style.cssText = 'margin-top: 16px; padding: 16px; background: var(--bg-tertiary); border-radius: 12px; border: 1px solid var(--border-color);';
        altSection.innerHTML = `
            <div style="font-size: 14px; font-weight: 700; color: var(--text-primary); margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>🔍</span>
                <span>Alternative Diagnoses</span>
            </div>
            <div style="display: grid; gap: 8px;">
                ${prediction.top_predictions.slice(1, 4).map((pred, idx) => `
                    <div style="padding: 10px; background: var(--bg-secondary); border-radius: 8px; font-size: 13px; color: var(--text-secondary); display: flex; justify-content: space-between; align-items: center;">
                        <span>${idx + 2}. <strong style="color: var(--text-primary);">${pred.plant}</strong> - ${pred.disease}</span>
                        <span style="font-weight: 600; color: var(--accent-primary);">${pred.confidence}</span>
                    </div>
                `).join('')}
            </div>
            <div style="margin-top: 12px; font-size: 12px; color: var(--text-tertiary); font-style: italic;">
                💡 These are alternative possibilities based on the image analysis
            </div>
        `;
        div.querySelector('div').appendChild(altSection);
    }
    
    chatBody.appendChild(div);
    scrollToBottom();
}
// Add image thumbnail (smaller, less prominent)
function addImageThumbnail(imageUrl) {
    const chatBody = document.getElementById('chatBody');
    if (!chatBody) return;
    
    const div = document.createElement('div');
    div.className = 'message bot image-thumbnail';
    div.innerHTML = `
        <div style="margin-bottom: 6px; color: var(--text-secondary); font-size: 12px;">
            📸 Uploaded Image
        </div>
        <img src="${SERVER_URL}${imageUrl}" 
             alt="Plant image"
             onclick="window.open('${SERVER_URL}${imageUrl}', '_blank')"
             style="max-width: 200px; max-height: 150px; border-radius: 8px; cursor: pointer; border: 1px solid var(--border-color); object-fit: cover;">
    `;
    chatBody.appendChild(div);
    scrollToBottom();
}

// Add formatted bot message with proper styling
function addFormattedBotMessage(text) {
    const chatBody = document.getElementById('chatBody');
    if (!chatBody) return;
    
    const div = document.createElement('div');
    div.className = 'message bot formatted';
    
    // Convert markdown-style formatting to HTML
    let formattedText = text
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>') // Bold
        .replace(/\n\n/g, '<br><br>') // Paragraphs
        .replace(/\n•/g, '<br>•') // Bullet points
        .replace(/\n/g, '<br>'); // Line breaks
    
    div.innerHTML = formattedText;
    chatBody.appendChild(div);
    scrollToBottom();
}

// Add message to DOM
function addMessageToDOM(content, sender) {
    const chatBody = document.getElementById('chatBody');
    if (!chatBody) return null;
    
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.textContent = content;
    div.id = 'msg-' + Date.now() + '-' + Math.random();
    chatBody.appendChild(div);
    scrollToBottom();
    
    return div.id;
}

// Add loading message
function addLoadingMessage() {
    const chatBody = document.getElementById('chatBody');
    if (!chatBody) return null;
    
    const div = document.createElement('div');
    div.className = 'message bot loading';
    div.id = 'msg-loading-' + Date.now();
    div.innerHTML = `
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    `;
    chatBody.appendChild(div);
    scrollToBottom();
    
    return div.id;
}

// Remove message
function removeMessage(id) {
    const msg = document.getElementById(id);
    if (msg) {
        msg.remove();
    }
}

// Update send button state
function updateSendButton(disabled) {
    const sendBtn = document.getElementById('sendBtn');
    if (sendBtn) {
        sendBtn.disabled = disabled;
    }
}

// Scroll to bottom
function scrollToBottom() {
    const chatBody = document.getElementById('chatBody');
    if (chatBody) {
        setTimeout(() => {
            chatBody.scrollTop = chatBody.scrollHeight;
        }, 100);
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}