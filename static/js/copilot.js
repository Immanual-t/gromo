// Sales Co-Pilot JavaScript for FinArva AI

// Store conversation context
let conversationContext = [];
let transcriptStarted = false;
let customerType = '';
let productType = '';

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the sales co-pilot
    initSalesCopilot();

    // Setup form submission
    setupFormSubmission();

    // Setup product selection
    setupProductSelection();

    // Setup conversation controls
    setupConversationControls();
});

// Initialize the sales co-pilot
function initSalesCopilot() {
    // Get DOM elements
    const startTranscriptBtn = document.getElementById('startTranscript');
    const customerTypeSelect = document.getElementById('customerType');
    const productTypeSelect = document.getElementById('productType');

    // Enable/disable start button based on selections
    function checkFormValidity() {
        startTranscriptBtn.disabled = !(customerTypeSelect.value && productTypeSelect.value);
    }

    // Add event listeners
    customerTypeSelect.addEventListener('change', checkFormValidity);
    productTypeSelect.addEventListener('change', checkFormValidity);

    // Initial check
    checkFormValidity();

    // Setup start transcript button
    startTranscriptBtn.addEventListener('click', function() {
        customerType = customerTypeSelect.value;
        productType = productTypeSelect.value;

        // Show conversation interface
        document.getElementById('setupForm').classList.add('d-none');
        document.getElementById('conversationInterface').classList.remove('d-none');

        // Start conversation
        startConversation(customerType, productType);
    });
}

// Start the conversation
function startConversation(customerType, productType) {
    // Add system message to context
    conversationContext = [{
        role: 'system',
        content: `You are an AI sales assistant helping a GroMo Partner (GP) sell financial products in India.
        The GP is currently talking to a ${customerType} customer about a ${productType} product.
        Provide real-time sales suggestions, objection handling tips, and product information to help the GP close the sale.
        Keep suggestions brief, practical, and tailored to the Indian market context.`
    }];

    transcriptStarted = true;

    // Display initial greeting and tips
    displayAIMessage("I'm your sales co-pilot for this conversation! As you talk with your customer, I'll provide real-time suggestions to help you close the sale. Start by sharing what the customer is saying, and I'll guide you.");

    // Add initial tips based on customer and product type
    generateInitialTips(customerType, productType);
}

// Generate initial tips based on customer and product type
function generateInitialTips(customerType, productType) {
    // Create a message for the AI
    const prompt = `Give me 3 quick tips for selling ${productType} to a ${customerType} customer in India. Format as bullet points.`;

    // Add to context
    conversationContext.push({
        role: 'user',
        content: prompt
    });

    // Show loading state
    const loadingMessage = document.createElement('div');
    loadingMessage.className = 'chat-message ai d-flex mb-3';
    loadingMessage.innerHTML = `
        <div class="spinner-border text-primary spinner-border-sm me-2" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        <div>Generating initial tips...</div>
    `;
    document.getElementById('chatMessages').appendChild(loadingMessage);

    // Scroll to bottom
    scrollToBottom();

    // Send to API
    fetch('/ai-assistant/generate-suggestion/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            messages: conversationContext
        })
    })
    .then(response => response.json())
    .then(data => {
        // Remove loading message
        document.getElementById('chatMessages').removeChild(loadingMessage);

        // Display AI response
        displayAIMessage(data.response);

        // Add to context
        conversationContext.push({
            role: 'assistant',
            content: data.response
        });
    })
    .catch(error => {
        console.error('Error:', error);
        // Remove loading message
        document.getElementById('chatMessages').removeChild(loadingMessage);
        // Display error
        displayAIMessage("Sorry, I couldn't generate tips. Please try again.");
    });
}

// Setup form submission
function setupFormSubmission() {
    const messageForm = document.getElementById('messageForm');
    const userMessageInput = document.getElementById('userMessage');

    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const userMessage = userMessageInput.value.trim();
        if (!userMessage) return;

        // Display user message
        displayUserMessage(userMessage);

        // Add to context
        conversationContext.push({
            role: 'user',
            content: userMessage
        });

        // Clear input
        userMessageInput.value = '';

        // Generate AI response
        generateAIResponse();
    });
}

// Display user message in chat
function displayUserMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'd-flex flex-column align-items-end mb-3';
    messageElement.innerHTML = `
        <div class="chat-message user">
            <div class="small text-muted mb-1">You</div>
            <div>${message}</div>
        </div>
    `;
    document.getElementById('chatMessages').appendChild(messageElement);

    // Scroll to bottom
    scrollToBottom();
}

// Display AI message in chat
function displayAIMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'd-flex flex-column mb-3';
    messageElement.innerHTML = `
        <div class="chat-message ai">
            <div class="small text-muted mb-1">FinArva AI</div>
            <div>${message}</div>
        </div>
    `;
    document.getElementById('chatMessages').appendChild(messageElement);

    // Scroll to bottom
    scrollToBottom();
}

// Generate AI response
function generateAIResponse() {
    // Show loading state
    const loadingMessage = document.createElement('div');
    loadingMessage.className = 'chat-message ai d-flex mb-3';
    loadingMessage.innerHTML = `
        <div class="spinner-border text-primary spinner-border-sm me-2" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        <div>Thinking...</div>
    `;
    document.getElementById('chatMessages').appendChild(loadingMessage);

    // Scroll to bottom
    scrollToBottom();

    // Send to API
    fetch('/ai-assistant/generate-suggestion/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            messages: conversationContext
        })
    })
    .then(response => response.json())
    .then(data => {
        // Remove loading message
        document.getElementById('chatMessages').removeChild(loadingMessage);

        // Display AI response
        displayAIMessage(data.response);

        // Add to context
        conversationContext.push({
            role: 'assistant',
            content: data.response
        });
    })
    .catch(error => {
        console.error('Error:', error);
        // Remove loading message
        document.getElementById('chatMessages').removeChild(loadingMessage);
        // Display error
        displayAIMessage("Sorry, I couldn't generate a response. Please try again.");
    });
}

// Setup product selection
function setupProductSelection() {
    const productTypeSelect = document.getElementById('productType');

    // When product type changes, update the objection list
    productTypeSelect.addEventListener('change', function() {
        updateObjectionList(this.value);
    });

    // Initial update
    updateObjectionList(productTypeSelect.value);
}

// Update the common objections list based on product
function updateObjectionList(productType) {
    const objectionList = document.getElementById('commonObjections');
    if (!objectionList) return;

    // Clear current list
    objectionList.innerHTML = '';

    // Define objections for each product type
    const objections = {
        'insurance': [
            "I already have insurance",
            "The premium is too high",
            "I don't trust insurance companies",
            "I don't understand the policy terms"
        ],
        'credit_card': [
            "I already have too many credit cards",
            "I'm worried about the interest rates",
            "I don't want to pay annual fees",
            "I don't spend enough to justify rewards"
        ],
        'loan': [
            "The interest rate is too high",
            "I'm concerned about hidden charges",
            "The documentation process is too complex",
            "I'm worried about my credit score"
        ],
        'investment': [
            "The market is too volatile right now",
            "I don't understand the risk involved",
            "I can't lock my money for that long",
            "The returns are not guaranteed"
        ]
    };

    // Get objections for the selected product
    const productObjections = objections[productType] || [];

    // Add objections to list
    productObjections.forEach(objection => {
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-outline-secondary mb-2 me-2';
        button.innerText = objection;
        button.addEventListener('click', function() {
            handleObjection(objection);
        });
        objectionList.appendChild(button);
    });
}

// Handle objection click
function handleObjection(objection) {
    // Create a message for the AI
    const prompt = `Customer objection: "${objection}". How should I respond?`;

    // Display user message
    displayUserMessage(prompt);

    // Add to context
    conversationContext.push({
        role: 'user',
        content: prompt
    });

    // Generate AI response
    generateAIResponse();
}

// Setup conversation controls
function setupConversationControls() {
    // Reset conversation button
    const resetBtn = document.getElementById('resetConversation');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            // Confirm reset
            if (confirm('Are you sure you want to reset the conversation? This will clear all messages.')) {
                // Clear chat messages
                document.getElementById('chatMessages').innerHTML = '';

                // Go back to setup form
                document.getElementById('conversationInterface').classList.add('d-none');
                document.getElementById('setupForm').classList.remove('d-none');

                // Reset conversation context
                conversationContext = [];
                transcriptStarted = false;
            }
        });
    }

    // Save conversation button
    const saveBtn = document.getElementById('saveConversation');
    if (saveBtn) {
        saveBtn.addEventListener('click', function() {
            // Create a download link
            const conversationText = conversationContext
                .filter(msg => msg.role !== 'system')
                .map(msg => `${msg.role === 'user' ? 'You' : 'AI'}: ${msg.content}`)
                .join('\n\n');

            const blob = new Blob([conversationText], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = `sales-conversation-${new Date().toISOString().slice(0, 10)}.txt`;
            document.body.appendChild(a);
            a.click();

            setTimeout(() => {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }, 0);
        });
    }
}

// Helper function to get CSRF token
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Helper function to scroll chat to bottom
function scrollToBottom() {
    const chatContainer = document.getElementById('chatMessages');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}