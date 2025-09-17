// Voice Assistance for KrishiVaani App with Multi-Language Support
// Uses Web Speech API for speech recognition and synthesis

// Global language settings
let currentLanguage = localStorage.getItem('voiceLanguage') || 'en-IN';
let currentLangCode = localStorage.getItem('voiceLangCode') || 'EN';

// Multi-language text translations
const translations = {
    'en-IN': {
        welcome: 'Hello! I am your KrishiVaani voice assistant. Where would you like to go?',
        listening: '🎤 Listening...',
        processing: '⚡ Processing...',
        clickToSpeak: '👂 Click to speak',
        browserNotSupported: 'Sorry, your browser does not support voice recognition.',
        errorOccurred: '❌ Error occurred',
        voiceError: 'Voice recognition error: ',
        dashboardHelp: 'I can help you with dashboard features like crop recommendation, yield prediction, crop planning, price tracker, disease prediction, forum, labour alerts, crop calendar, AI chat, weather, disease guide, organic farming, plantation guide, farmer portal, or shopkeeper portal.',
        generalHelp: 'I can help you navigate to different pages. Try saying: dashboard, login, about, contact, weather, disease detection, organic farming, plantation guide, farmer portal, or shopkeeper portal.',
        notUnderstood: 'I did not understand that command. Try saying dashboard, login, about, contact, or help for available options.',
        dashboardNotUnderstood: 'I did not understand that command. Try saying crop recommendation, yield prediction, crop planning, price tracker, disease prediction, forum, weather, or help for available options.',
        navigatingTo: 'Navigating to ',
        opening: 'Opening '
    },
    'hi-IN': {
        welcome: 'नमस्कार! मैं आपका कृषिवाणी आवाज सहायक हूं। आप कहां जाना चाहेंगे?',
        listening: '🎤 सुन रहा हूं...',
        processing: '⚡ प्रोसेसिंग...',
        clickToSpeak: '👂 बोलने के लिए क्लिक करें',
        browserNotSupported: 'क्षमा करें, आपका ब्राउज़र आवाज पहचान का समर्थन नहीं करता।',
        errorOccurred: '❌ त्रुटि हुई',
        voiceError: 'आवाज पहचान त्रुटि: ',
        dashboardHelp: 'मैं डैशबोर्ड सुविधाओं जैसे फसल सिफारिश, उत्पादन पूर्वानुमान, फसल योजना, मूल्य ट्रैकर, रोग पूर्वानुमान, फोरम, श्रम अलर्ट, फसल कैलेंडर में मदद कर सकता हूं।',
        generalHelp: 'मैं विभिन्न पृष्ठों पर नेविगेट करने में मदद कर सकता हूं। कहें: डैशबोर्ड, लॉगिन, बारे में, संपर्क, मौसम, रोग का पता लगाना।',
        notUnderstood: 'मैं उस कमांड को नहीं समझा। डैशबोर्ड, लॉगिन, बारे में, संपर्क, या सहायता कहने की कोशिश करें।',
        dashboardNotUnderstood: 'मैं उस कमांड को नहीं समझा। फसल सिफारिश, उत्पादन पूर्वानुमान, या सहायता कहने की कोशिश करें।',
        navigatingTo: 'जा रहे हैं ',
        opening: 'खोल रहे हैं '
    },
    'bn-IN': {
        welcome: 'নমস্কার! আমি আপনার কৃষিবাণী ভয়েস সহায়ক। আপনি কোথায় যেতে চান?',
        listening: '🎤 শুনছি...',
        processing: '⚡ প্রক্রিয়াকরণ...',
        clickToSpeak: '👂 কথা বলতে ক্লিক করুন',
        browserNotSupported: 'দুঃখিত, আপনার ব্রাউজার ভয়েস রিকগনিশন সাপোর্ট করে না।',
        errorOccurred: '❌ ত্রুটি ঘটেছে',
        voiceError: 'ভয়েস রিকগনিশন ত্রুটি: ',
        dashboardHelp: 'আমি ড্যাশবোর্ড বৈশিষ্ট্য যেমন ফসল সুপারিশ, ফলন পূর্বাভাস, ফসল পরিকল্পনা নিয়ে সহায়তা করতে পারি।',
        generalHelp: 'আমি বিভিন্ন পৃষ্ঠায় নেভিগেট করতে সাহায্য করতে পারি। বলুন: ড্যাশবোর্ড, লগইন, সম্পর্কে।',
        notUnderstood: 'আমি সেই কমান্ডটি বুঝতে পারিনি। ড্যাশবোর্ড, লগইন, সাহায্য বলার চেষ্টা করুন।',
        dashboardNotUnderstood: 'আমি সেই কমান্ডটি বুঝতে পারিনি। ফসল সুপারিশ, ফলন পূর্বাভাস বলার চেষ্টা করুন।',
        navigatingTo: 'যাচ্ছি ',
        opening: 'খুলছি '
    },
    'te-IN': {
        welcome: 'నమస్కారం! నేను మీ కృషివాణి వాయిస్ అసిస్టెంట్. మీరు ఎక్కడికి వెళ్లాలని అనుకుంటున్నారు?',
        listening: '🎤 వింటున్నాను...',
        processing: '⚡ ప్రాసెసింగ్...',
        clickToSpeak: '👂 మాట్లాడటానికి క్లిక్ చేయండి',
        browserNotSupported: 'క్షమించండి, మీ బ్రౌజర్ వాయిస్ రికగ్నిషన్‌ను సపోర్ట్ చేయదు।',
        errorOccurred: '❌ లోపం సంభవించింది',
        voiceError: 'వాయిస్ రికగ్నిషన్ లోపం: ',
        dashboardHelp: 'నేను డాష్‌బోర్డ్ ఫీచర్లు అయిన పంట సిఫార్సు, దిగుబడి అంచనా, పంట ప్రణాళికలో సహాయం చేయగలను।',
        generalHelp: 'నేను వివిధ పేజీలకు నావిగేట్ చేయడంలో సహాయం చేయగలను। చెప్పండి: డాష్‌బోర్డ్, లాగిన్।',
        notUnderstood: 'నేను ఆ కమాండ్‌ను అర్థం చేసుకోలేకపోయాను. డాష్‌బోర్డ్, లాగిన్ అని చెప్పండి।',
        dashboardNotUnderstood: 'నేను ఆ కమాండ్‌ను అర్థం చేసుకోలేకపోయాను। పంట సిఫార్సు అని చెప్పండి।',
        navigatingTo: 'వెళ్తున్నాము ',
        opening: 'తెరుస్తున్నాము '
    },
    'mr-IN': {
        welcome: 'नमस्कार! मी तुमचा कृषिवाणी आवाज सहाय्यक आहे. तुम्ही कुठे जाऊ इच्छिता?',
        listening: '🎤 ऐकत आहे...',
        processing: '⚡ प्रक्रिया करत आहे...',
        clickToSpeak: '👂 बोलण्यासाठी क्लिक करा',
        browserNotSupported: 'क्षमस्व, तुमचा ब्राउझर आवाज ओळख समर्थित करत नाही.',
        errorOccurred: '❌ त्रुटी झाली',
        voiceError: 'आवाज ओळख त्रुटी: ',
        dashboardHelp: 'मी डॅशबोर्ड वैशिष्ट्ये जसे की पिक शिफारस, उत्पादन अंदाज यामध्ये मदत करू शकतो.',
        generalHelp: 'मी विविध पृष्ठांवर नेव्हिगेट करण्यात मदत करू शकतो. म्हणा: डॅशबोर्ड, लॉगिन.',
        notUnderstood: 'मला तो आदेश समजला नाही. डॅशबोर्ड, लॉगिन म्हणून पहा.',
        dashboardNotUnderstood: 'मला तो आदेश समजला नाही. पीक शिफारस म्हणून पहा.',
        navigatingTo: 'जात आहे ',
        opening: 'उघडत आहे '
    },
    'ta-IN': {
        welcome: 'வணக்கம்! நான் உங்கள் கிருஷிவாணி குரல் உதவியாளர். நீங்கள் எங்கு செல்ல விரும்புகிறீர்கள்?',
        listening: '🎤 கேட்டுக்கொண்டிருக்கிறேன்...',
        processing: '⚡ செயலாக்கம்...',
        clickToSpeak: '👂 பேச கிளிக் செய்யவும்',
        browserNotSupported: 'மன்னிக்கவும், உங்கள் உலாவி குரல் அடையாளத்தை ஆதரிக்கவில்லை.',
        errorOccurred: '❌ பிழை ஏற்பட்டது',
        voiceError: 'குரல் அடையாள பிழை: ',
        dashboardHelp: 'நான் டாஷ்போர்டு அம்சங்களான பயிர் பரிந்துரை, மகசூல் முன்னறிவிப்பில் உதவ முடியும்.',
        generalHelp: 'நான் வெவ்வேறு பக்கங்களுக்கு செல்ல உதவ முடியும். சொல்லுங்கள்: டாஷ்போர்டு, உள்நுழைவு.',
        notUnderstood: 'அந்த கட்டளையை என்னால் புரிந்துகொள்ள முடியவில்லை. டாஷ்போர்டு என்று சொல்லுங்கள்.',
        dashboardNotUnderstood: 'அந்த கட்டளையை என்னால் புரிந்துகொள்ள முடியவில்லை. பயிர் பரிந்துரை என்று சொல்லுங்கள்.',
        navigatingTo: 'செல்கிறோம் ',
        opening: 'திறக்கிறோம் '
    }
};

function speak(text, language = currentLanguage) {
    if ('speechSynthesis' in window) {
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = language;
        utter.rate = 0.9;
        utter.pitch = 1.0;
        window.speechSynthesis.speak(utter);
    }
}

function getTranslation(key, language = currentLanguage) {
    return translations[language]?.[key] || translations['en-IN'][key] || key;
}

function startRecognition(targetInput, promptText) {
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        speak(getTranslation('browserNotSupported'));
        return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = currentLanguage;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    speak(promptText);
    recognition.start();
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript.trim();
        targetInput.value = transcript;
        speak(getTranslation('opening') + transcript);
    };
    recognition.onerror = function(event) {
        speak(getTranslation('voiceError') + event.error);
    };
}

// Voice Navigation for Main App
function handleVoiceCommand(command) {
    const cmd = command.toLowerCase().trim();
    const currentPage = window.location.pathname.split('/').pop();
    
    // Dashboard-specific commands
    if (currentPage === 'dashboard.html') {
        if (cmd.includes('crop recommendation') || cmd.includes('recommend crop') || cmd.includes('फसल सिफारिश') || cmd.includes('ফসল সুপারিশ') || cmd.includes('పంట సిఫార్సు') || cmd.includes('पीक शिफारस') || cmd.includes('பயிர் பரிந்துரை')) {
            speak(getTranslation('opening') + 'crop recommendation system');
            window.location.href = 'Crop Recommendation/templates/index.html';
        } else if (cmd.includes('yield prediction') || cmd.includes('predict yield') || cmd.includes('उत्पादन पूर्वानुमान') || cmd.includes('ফলন পূর্বাভাস') || cmd.includes('దిగుబడి అంచనా') || cmd.includes('उत्पादन अंदाज') || cmd.includes('மகசூல் முன்னறிவிப்பு')) {
            speak(getTranslation('opening') + 'crop yield prediction');
            window.location.href = 'Crop Yield Prediction/templates/index.html';
        } else if (cmd.includes('crop planning') || cmd.includes('plan crop') || cmd.includes('फसल योजना') || cmd.includes('ফসল পরিকল্পনা') || cmd.includes('పంట ప్రణాళిక') || cmd.includes('पीक योजना') || cmd.includes('பயிர் திட்டம்')) {
            speak(getTranslation('opening') + 'crop planning tool');
            window.location.href = 'Crop_Planning/templates/cropplan.html';
        } else if (cmd.includes('price tracker') || cmd.includes('crop price') || cmd.includes('मूल्य ट्रैकर') || cmd.includes('দাম ট্র্যাকার') || cmd.includes('ధర ట్రాకర్') || cmd.includes('किंमत ट्रॅकर') || cmd.includes('விலை கண்காணிப்பாளர்')) {
            speak(getTranslation('opening') + 'crop price tracker');
            window.location.href = 'Crop_Prices_Tracker/templates/crop_price_tracker.html';
        } else if (cmd.includes('disease prediction') || cmd.includes('detect disease') || cmd.includes('रोग पूर्वानुमान') || cmd.includes('রোগ পূর্বাভাস') || cmd.includes('వ్యాధి అంచనా') || cmd.includes('रोग पूर्वानुमान') || cmd.includes('நோய் கணிப்பு')) {
            speak(getTranslation('opening') + 'disease prediction system');
            window.location.href = 'Decises_Prediction/template/index.html';
        } else if (cmd.includes('forum') || cmd.includes('community') || cmd.includes('फोरम') || cmd.includes('ফোরাম') || cmd.includes('ఫోరమ్') || cmd.includes('फोरम') || cmd.includes('மன்றம்')) {
            speak(getTranslation('opening') + 'community forum');
            window.location.href = 'Forum/forum.html';
        } else if (cmd.includes('labour alerts') || cmd.includes('labor alert') || cmd.includes('श्रम अलर्ट') || cmd.includes('শ্রম সতর্কতা') || cmd.includes('కార్మిక హెచ్చరికలు') || cmd.includes('श्रम अलर्ट') || cmd.includes('தொழிலாளர் எச்சரிக்கைகள்')) {
            speak(getTranslation('opening') + 'labour alerts');
            window.location.href = 'Labour_Alerts/tamplates/labour-alerts.html';
        } else if (cmd.includes('calendar') || cmd.includes('crop calendar') || cmd.includes('कैलेंडर') || cmd.includes('ক্যালেন্ডার') || cmd.includes('క్యాలెండర్') || cmd.includes('कैलेंडर') || cmd.includes('நாட்காட்டி')) {
            speak(getTranslation('opening') + 'crop calendar');
            window.location.href = 'cropCalendar.html';
        } else if (cmd.includes('chat') || cmd.includes('ai chat') || cmd.includes('चैट') || cmd.includes('চ্যাট') || cmd.includes('చాట్') || cmd.includes('चैट') || cmd.includes('அரட்டை')) {
            speak(getTranslation('opening') + 'AI chat assistant');
            window.location.href = 'chat.html';
        }
        // Continue with general navigation commands
        else if (cmd.includes('weather')) {
            speak('Navigating to weather information');
            window.location.href = 'weather.html';
        } else if (cmd.includes('disease guide') || cmd.includes('plant disease guide')) {
            speak('Navigating to disease guide');
            window.location.href = 'disease.html';
        } else if (cmd.includes('organic') || cmd.includes('organic farming')) {
            speak('Navigating to organic farming guide');
            window.location.href = 'organic.html';
        } else if (cmd.includes('plantation') || cmd.includes('plant guide')) {
            speak('Navigating to plantation guide');
            window.location.href = 'plantation.html';
        } else if (cmd.includes('farmer portal') || cmd.includes('farmers')) {
            speak('Navigating to farmer portal');
            window.location.href = 'farmer.html';
        } else if (cmd.includes('shopkeeper') || cmd.includes('shop keeper')) {
            speak('Navigating to shopkeeper portal');
            window.location.href = 'shopkeeper.html';
        } else if (cmd.includes('help') || cmd.includes('what can you do') || cmd.includes('मदद') || cmd.includes('সাহায্য') || cmd.includes('సహాయం') || cmd.includes('मदत') || cmd.includes('உதவி')) {
            speak(getTranslation('dashboardHelp'));
        } else {
            speak(getTranslation('dashboardNotUnderstood'));
        }
    }
    // General navigation commands for all pages
    else {
        if (cmd.includes('dashboard') || cmd.includes('dash board')) {
            speak('Navigating to dashboard');
            window.location.href = 'dashboard.html';
        } else if (cmd.includes('login') || cmd.includes('log in')) {
            speak('Navigating to login page');
            window.location.href = 'login.html';
        } else if (cmd.includes('about') || cmd.includes('about us')) {
            speak('Navigating to about page');
            window.location.href = 'about.html';
        } else if (cmd.includes('contact') || cmd.includes('feedback')) {
            speak('Navigating to contact page');
            window.location.href = 'feed-back.html';
        } else if (cmd.includes('weather')) {
            speak('Navigating to weather information');
            window.location.href = 'weather.html';
        } else if (cmd.includes('disease') || cmd.includes('plant disease')) {
            speak('Navigating to disease detection');
            window.location.href = 'disease.html';
        } else if (cmd.includes('organic') || cmd.includes('organic farming')) {
            speak('Navigating to organic farming guide');
            window.location.href = 'organic.html';
        } else if (cmd.includes('plantation') || cmd.includes('plant')) {
            speak('Navigating to plantation guide');
            window.location.href = 'plantation.html';
        } else if (cmd.includes('farmer') || cmd.includes('farmers')) {
            speak('Navigating to farmer portal');
            window.location.href = 'farmer.html';
        } else if (cmd.includes('shopkeeper') || cmd.includes('shop keeper')) {
            speak('Navigating to shopkeeper portal');
            window.location.href = 'shopkeeper.html';
        } else if (cmd.includes('home') || cmd.includes('homepage')) {
            speak('Navigating to homepage');
            window.location.href = 'index.html';
        } else if (cmd.includes('help') || cmd.includes('what can you do') || cmd.includes('मदद') || cmd.includes('সাহায্য') || cmd.includes('సహాయం') || cmd.includes('मदत') || cmd.includes('உதவி')) {
            speak(getTranslation('generalHelp'));
        } else {
            speak(getTranslation('notUnderstood'));
        }
    }
}

function updateVoiceStatus(status, text) {
    const voiceStatus = document.getElementById('voiceStatus');
    const statusText = voiceStatus?.querySelector('.status-text');
    
    if (voiceStatus && statusText) {
        voiceStatus.className = `voice-status ${status} show`;
        statusText.textContent = text;
        
        if (status === 'listening' || status === 'processing') {
            setTimeout(() => {
                voiceStatus.classList.remove('show');
            }, status === 'listening' ? 5000 : 3000);
        } else {
            setTimeout(() => {
                voiceStatus.classList.remove('show');
            }, 2000);
        }
    }
}

function startVoiceAssistant() {
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        speak(getTranslation('browserNotSupported'));
        updateVoiceStatus('error', getTranslation('browserNotSupported'));
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = currentLanguage;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    
    const voiceIcon = document.getElementById('voiceIcon');
    const voiceBtn = document.getElementById('voiceAssistant');
    
    // Update button state to listening
    if (voiceIcon && voiceBtn) {
        voiceIcon.className = 'fas fa-microphone-slash';
        voiceBtn.classList.remove('processing');
        voiceBtn.classList.add('listening');
    }
    
    updateVoiceStatus('listening', getTranslation('listening'));
    speak(getTranslation('welcome'));
    
    recognition.start();
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript.trim();
        console.log('Voice command:', transcript);
        
        // Update to processing state
        if (voiceBtn) {
            voiceBtn.classList.remove('listening');
            voiceBtn.classList.add('processing');
        }
        
        updateVoiceStatus('processing', getTranslation('processing'));
        
        setTimeout(() => {
            handleVoiceCommand(transcript);
            resetVoiceButton();
        }, 1000);
    };
    
    recognition.onerror = function(event) {
        speak(getTranslation('voiceError') + event.error);
        updateVoiceStatus('error', getTranslation('errorOccurred'));
        resetVoiceButton();
    };
    
    recognition.onend = function() {
        if (voiceBtn && voiceBtn.classList.contains('listening')) {
            resetVoiceButton();
            updateVoiceStatus('', getTranslation('clickToSpeak'));
        }
    };
}

function resetVoiceButton() {
    const voiceIcon = document.getElementById('voiceIcon');
    const voiceBtn = document.getElementById('voiceAssistant');
    
    if (voiceIcon && voiceBtn) {
        voiceIcon.className = 'fas fa-microphone';
        voiceBtn.classList.remove('listening', 'processing');
    }
}

// Language selector functionality
function initializeLanguageSelector() {
    const langToggle = document.getElementById('langToggle');
    const langDropdown = document.getElementById('langDropdown');
    const langText = document.querySelector('.lang-text');
    const langOptions = document.querySelectorAll('.lang-option');
    
    if (!langToggle || !langDropdown) return;
    
    // Set initial language
    langText.textContent = currentLangCode;
    
    // Mark current language as active
    langOptions.forEach(option => {
        if (option.dataset.lang === currentLanguage) {
            option.classList.add('active');
        }
    });
    
    // Toggle dropdown
    langToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        langDropdown.classList.toggle('show');
    });
    
    // Language selection
    langOptions.forEach(option => {
        option.addEventListener('click', (e) => {
            e.stopPropagation();
            
            // Update active language
            langOptions.forEach(opt => opt.classList.remove('active'));
            option.classList.add('active');
            
            // Update global settings
            currentLanguage = option.dataset.lang;
            currentLangCode = option.dataset.code;
            
            // Save to localStorage
            localStorage.setItem('voiceLanguage', currentLanguage);
            localStorage.setItem('voiceLangCode', currentLangCode);
            
            // Update UI
            langText.textContent = currentLangCode;
            langDropdown.classList.remove('show');
            
            // Update status text
            updateVoiceStatus('', getTranslation('clickToSpeak'));
            
            // Provide feedback
            speak(getTranslation('welcome'));
        });
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', () => {
        langDropdown.classList.remove('show');
    });
}

// Show/Hide Password functionality
function initializePasswordToggle() {
    const togglePasswordBtn = document.getElementById('togglePasswordBtn');
    const passwordInput = document.getElementById('password');
    const togglePasswordIcon = document.getElementById('togglePasswordIcon');
    
    if (togglePasswordBtn && passwordInput && togglePasswordIcon) {
        togglePasswordBtn.addEventListener('click', function() {
            const isPasswordVisible = passwordInput.type === 'text';
            
            if (isPasswordVisible) {
                // Hide password
                passwordInput.type = 'password';
                togglePasswordIcon.className = 'fas fa-eye';
                togglePasswordBtn.classList.remove('active');
                togglePasswordBtn.title = 'Show Password';
            } else {
                // Show password
                passwordInput.type = 'text';
                togglePasswordIcon.className = 'fas fa-eye-slash';
                togglePasswordBtn.classList.add('active');
                togglePasswordBtn.title = 'Hide Password';
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Initialize language selector
    initializeLanguageSelector();
    
    // Initialize password toggle
    initializePasswordToggle();
    
    // Main app voice assistant
    const voiceAssistant = document.getElementById('voiceAssistant');
    if (voiceAssistant) {
        voiceAssistant.addEventListener('click', startVoiceAssistant);
        
        // Initialize status text
        updateVoiceStatus('', getTranslation('clickToSpeak'));
    }
});