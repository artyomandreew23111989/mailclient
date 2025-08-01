document.getElementById('compose-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const to = this.elements[0].value;
    const subject = this.elements[1].value;
    const body = this.elements[2].value;

    const emailList = document.getElementById('email-list');
    const newEmail = document.createElement('li');
    newEmail.className = 'email-item';
    newEmail.innerHTML = `
        <span class="email-subject">${subject}</span>
        <button class="view-button" onclick="viewEmail('${subject}', '${body}')">Открыть</button>
    `;
    emailList.appendChild(newEmail);

    this.reset();
    alert('Письмо отправлено!');
});

function viewEmail(subject, body) {
    document.getElementById('modal-subject').innerText = subject;
    document.getElementById('modal-body').innerText = body;
    document.getElementById('modal').classList.remove('hidden');
}

document.getElementById('modal-close').addEventListener('click', function() {
    document.getElementById('modal').classList.add('hidden');
});
