document.addEventListener("DOMContentLoaded", function() {
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-theme");
        document.getElementById("themeIcon").classList.remove("fa-sun");
        document.getElementById("themeIcon").classList.add("fa-moon");
        document.getElementById("themeSwitch").checked = true;
    }
});

function toggleTheme() {
    document.body.classList.toggle("dark-theme");

    const themeIcon = document.getElementById("themeIcon");
    if (document.body.classList.contains("dark-theme")) {
        themeIcon.classList.remove("fa-sun");
        themeIcon.classList.add("fa-moon");
        localStorage.setItem("theme", "dark");
    } else {
        themeIcon.classList.remove("fa-moon");
        themeIcon.classList.add("fa-sun");
        localStorage.setItem("theme", "light");
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const background = document.querySelector('.background');
    const words = ['RuStore', 'Цифровой прорыв', 'ГИРЯ', 'СКФО'];
    const numColumns = 10;
    const numRows = 10;

    for (let i = 0; i < numRows; i++) {
        for (let j = 0; j < numColumns; j++) {
            const wordElement = document.createElement('div');
            wordElement.classList.add('word');
            wordElement.textContent = words[(i * numColumns + j) % words.length];
            background.appendChild(wordElement);
        }
    }

    const lastUpdate = localStorage.getItem('lastUpdate');
    const now = Date.now();
    
    if (lastUpdate) {
        const elapsedTime = (now - lastUpdate) / 1000;
        background.style.setProperty('--animation-start-time', `-${elapsedTime}s`);
    }
    localStorage.setItem('lastUpdate', now);
});


function addCopyButton(parentElement, messageText) {
    const copyButton = document.createElement('button');
    copyButton.innerHTML = '<i class="fas fa-copy"></i>';
    copyButton.classList.add('copy-button');
    copyButton.addEventListener('click', () => {
        navigator.clipboard.writeText(messageText).then(function() {
            console.log('Текст скопирован успешно: ' + messageText);
            showCopySuccessMessage();
        }, function(err) {
            console.error('Не удалось скопировать текст: ', err);
            alert('Не удалось скопировать текст :(');
        });
    });
    parentElement.appendChild(copyButton);
    parentElement.style.position = 'relative';
}

function showCopySuccessMessage() {
    const copySuccessMessage = document.createElement('div');
    copySuccessMessage.textContent = 'Текст скопирован успешно!';
    copySuccessMessage.classList.add('copy-success-message');
    document.body.appendChild(copySuccessMessage);
    setTimeout(() => {
        document.body.removeChild(copySuccessMessage);
    }, 2500);
}


function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();

    if (!message) return;
    input.value = '';

    let userMessages = JSON.parse(sessionStorage.getItem('userMessages')) || [];
    userMessages.push(message);
    sessionStorage.setItem('userMessages', JSON.stringify(userMessages));

    const userMessage = document.createElement('div');
    userMessage.className = 'message user';
    userMessage.textContent = message;
    document.getElementById('messages').appendChild(userMessage);

    document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;

    const botTyping = document.createElement('div');
    botTyping.className = 'message bot';

    const avatar = document.createElement('img');
    avatar.src = 'static/RuStore_Icon.svg';
    avatar.className = 'avatar';
    botTyping.appendChild(avatar);

    const typingIndicator = document.createElement('l-dot-wave');
    typingIndicator.setAttribute('size', '30');
    typingIndicator.setAttribute('speed', '1');
    typingIndicator.setAttribute('color', 'white');
    botTyping.appendChild(typingIndicator);

    document.getElementById('messages').appendChild(botTyping);

    document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
        setTimeout(() => {
            document.getElementById('messages').removeChild(botTyping);

            let botMessages = JSON.parse(sessionStorage.getItem('botMessages')) || [];
            botMessages.push(data.response);
            sessionStorage.setItem('botMessages', JSON.stringify(botMessages));

            const botMessage = document.createElement('div');
            botMessage.className = 'message bot';

            const botAvatar = document.createElement('img');
            botAvatar.src = 'static/RuStore_Icon.svg';
            botAvatar.className = 'avatar';
            botMessage.appendChild(botAvatar);

            const text = document.createElement('span');
            text.textContent = data.response;
            text.className = 'bot-text';
            botMessage.appendChild(text);
            addCopyButton(botMessage, data.response);
            document.getElementById('messages').appendChild(botMessage);

            document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
        }, 500);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    let userMessages = JSON.parse(sessionStorage.getItem('userMessages')) || [];
    let botMessages = JSON.parse(sessionStorage.getItem('botMessages')) || [];

    const messagesContainer = document.getElementById('messages');
    let messageCount = Math.max(userMessages.length, botMessages.length);

    for (let i = 0; i < messageCount; i++) {
        if (i < userMessages.length) {
            const userMessage = document.createElement('div');
            userMessage.className = 'message user';
            userMessage.textContent = userMessages[i];
            messagesContainer.appendChild(userMessage);
        }

        if (i < botMessages.length) {
            const botMessage = document.createElement('div');
            botMessage.className = 'message bot';

            const botAvatar = document.createElement('img');
            botAvatar.src = 'static/RuStore_Icon.svg';
            botAvatar.className = 'avatar';
            botMessage.appendChild(botAvatar);

            const text = document.createElement('span');
            text.textContent = botMessages[i];
            text.className = 'bot-text';
            botMessage.appendChild(text);
            addCopyButton(botMessage, botMessages[i]);
            messagesContainer.appendChild(botMessage);
        }
    }

messagesContainer.scrollTop = messagesContainer.scrollHeight;
});

function openDeleteConfirmationModal() {
    const modal = document.getElementById('deleteConfirmationModal');
    modal.style.display = 'block';

    const cancelButton = document.getElementById('cancelButton');
    const confirmButton = document.getElementById('confirmButton');

    cancelButton.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    confirmButton.addEventListener('click', function() {
        clearChat();
        modal.style.display = 'none';
    });
}