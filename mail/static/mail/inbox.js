document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click',() => compose_email('','',''));
  document.querySelector('#compose-form').addEventListener('submit',  send_mail);
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(a,b,c) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = a;
  document.querySelector('#compose-subject').value = b;
  document.querySelector('#compose-body').value = c;
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views

  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  const root = document.querySelector('#emails-view')
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(email => {
      const mail = document.createElement('div');
      mail.addEventListener('click', function() {
        fetch(`/emails/${email.id}`)
        .then(response => response.json())
        .then(email => {
          if (!email.read) {
            fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  read: !email.read
              })
            })
          }
          root.innerHTML = ""
          const sender = document.createElement('div')
          sender.innerHTML = `<strong>From:</strong> ${email.sender}`
          const recipients = document.createElement('div')
          recipients.innerHTML = `<strong>To:</strong> ${Object.assign(...email.recipients)}`
          const subject = document.createElement('div')
          subject.innerHTML = `<strong>Subject:</strong> ${email.subject}`
          const timestamp = document.createElement('div')
          timestamp.innerHTML = `<strong>Timestamp:</strong> ${email.timestamp}`
          const body = document.createElement('div')
          body.innerHTML = `${email.body}`
          root.append(sender)
          root.append(recipients)
          root.append(subject)
          root.append(timestamp)
          const buttonRep = document.createElement('button')
          buttonRep.innerHTML = 'reply'
          buttonRep.classList.add("btn");
          buttonRep.classList.add("btn-sm");
          buttonRep.classList.add("btn-outline-primary");
          buttonRep.addEventListener('click', () => {
            root.innerHTML = ""
            compose_email(email.sender,`Re:${Object.assign(...email.recipients)}`,`${email.timestamp} ${email.sender} wrote:${email.body}`)
          })
          const buttonArch = document.createElement('button')
          buttonArch.innerHTML =  email.archived ? "Unarchive": 'Archive'
          let cssstyle = email.archived ? "btn-outline-success": "btn-outline-danger"
          buttonArch.classList.add("btn","btn-sm",cssstyle,"ml-1");
          buttonArch.addEventListener('click', () => {
            fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  archived: !email.archived
              })
            })
            .then(()=>load_mailbox('inbox'))
          })
          root.append(buttonRep)
          root.append(buttonArch)
          hr = document.createElement('hr')
          root.append(hr)
          root.append(body)
            console.log(email);
        });
      });
      mail.className = "mail";
      if (email.read === false) mail.style.backgroundColor = '#B8B8B8';
      const leftside = document.createElement('div');
      const righttside = document.createElement('div');
      const emailName = document.createElement('span');
      const text = document.createElement('span');
      const time = document.createElement('span');
      emailName.innerHTML = email.sender
      time.innerHTML = email.timestamp
      text.innerHTML = `\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0${email.body}`
      leftside.append(emailName)
      leftside.append(text)
      righttside.append(time)
      mail.append(leftside)
      mail.append(righttside)
      root.append(mail)
    });
});
} 

function send_mail(e){
  const recipients = document.querySelector('#compose-recipients').value
  const subject = document.querySelector('#compose-subject').value
  const body = document.querySelector('#compose-body').value
  e.preventDefault()
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      console.log(result);
      load_mailbox('inbox')
  });
  console.log(recipients)
  console.log(subject)
  console.log(body)
}