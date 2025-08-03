document.addEventListener('DOMContentLoaded', function() {
    loadEmails();

    document.getElementById('compose-form').addEventListener('submit', function(event) {
        event.preventDefault();
        sendEmail();
    });

    const socket = new WebSocket('ws://' + window.location.host + '/ws/emails/');

    socket.onmessage = function(event) {
        const email = JSON.parse(event.data);
        prependEmail(email);
    };

    socket.onclose = function(event) {
        console.error('WebSocket closed unexpectedly');
    };
});

function loadEmails() {
    fetch('/api/emails/')
        .then(response => response.json())
        .then(data => {
            const emailList = document.getElementById('email-list');
            emailList.innerHTML = '';
            data.forEach(email => {
                appendEmail(email);
            });
        });
}

function sendEmail() {
    const to = document.getElementById('to').value;
    const subject = document.getElementById('subject').value;
    const body = document.getElementById('body').value;

    fetch('/api/emails/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ to, subject, body })
    })
    .then(response => response.json())
    .then(data => {
        alert('Письмо отправлено!');
        document.getElementById('compose-form').reset();
        // Не вызываем loadEmails() — обновление придёт по WebSocket
    });
}

function appendEmail(email) {
    const emailList = document.getElementById('email-list');
    const li = document.createElement('li');
    li.className = 'email-item';
    li.innerHTML = `
        <span class="email-subject">${email.subject}</span>
        <button class="view-button" onclick="alert('${email.body.replace(/'/g, "\\'")}')">Открыть</button>
    `;
    emailList.appendChild(li);
}

function prependEmail(email) {
    const emailList = document.getElementById('email-list');
    const li = document.createElement('li');
    li.className = 'email-item';
    li.innerHTML = `
        <span class="email-subject">${email.subject}</span>
        <button class="view-button" onclick="alert('${email.body.replace(/'/g, "\\'")}')">Открыть</button>
    `;
    emailList.insertBefore(li, emailList.firstChild);
}

function getCSRFToken() {
    let csrfToken = null;
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            csrfToken = value;
        }
    }
    return csrfToken;
}
