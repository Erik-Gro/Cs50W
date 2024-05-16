
let container = document.querySelector(".messagesection")

let anketessec = document.querySelector(".anketessec")

let divtextarea = document.querySelector(".divtextarea")

let numberofmessages = 0

let currentchatid = 0

let notevenclicked = true

let matches = 0

let nextelementinarray = 0

let chatroomid = 0

function myCallback() {
  loadmessages(currentchatid)
}

let intervalID = 0

function loadmessages(id){
  chatroomid = id
  anketessec.style.display = "none";
  container.style.display = "block";
  if(notevenclicked===true){
    divtextarea.style.display = "block";
    notevenclicked = false
    console.log('setted')
    intervalID = setInterval(myCallback, 1000, );
  }
    fetch(`/loadmessagges/${id}`,{
        method: 'POST',
    })
  .then(response =>  response.json())
  .then(messages => {
    if(messages.length > numberofmessages || id !== currentchatid){
      console.log('worked')
    container.innerHTML = ''
    numberofmessages = 0
      for(message of messages){
      numberofmessages ++
      const div = document.createElement('h1')
      div.innerText = message.sender + ":" + message.text 
      console.log(div)
      container.append(div)
    }
    currentchatid = id
    container.scrollTop = container.scrollHeight;
  }
})
}

function findmatches(id){
  container.innerHTML = ''
  notevenclicked = true
  numberofmessages = 0
  id = 0
  divtextarea.style.display = "none";
  clearInterval(intervalID)
  fetch(`/loadcards/${id}`,{
    method: 'POST',
})
.then(response =>  response.json())
.then(people => {
  matches = people
  console.log(matches)
  nextmatch(matches[nextelementinarray])
})
}

function nextmatch(man){
  nextelementinarray++
  anketessec.innerHTML = ''
  // notevenclicked = true
  anketessec.style.display = "block";
  container.style.display = "none";
  console.log(man)
  const root = document.createElement('div');
  const anotherdiv = document.createElement('div');
  const divimg = document.createElement('div');
  divimg.classList.add("poscenter")
  const oImg = document.createElement("img");
  oImg.setAttribute('src', `${man.img}`);
  oImg.classList.add("mystyle");
  divimg.append(oImg)
  root.append(divimg)
  const btnskip = document.createElement("button");
  const btnadd = document.createElement("button");
  btnskip.innerText = "skip"
  btnadd.innerText = "Like"
  anotherdiv.classList.add("buttons",)
  anotherdiv.append(btnskip)
  anotherdiv.append(btnadd)
  btnskip.classList.add("poscenter","btn","btn-warning",)
  btnadd.classList.add("poscenter","btn","btn-success",)
  btnskip.addEventListener('click', function() {
    nextmatch(matches[nextelementinarray])
  })
  btnadd.addEventListener('click', function() {
    console.log(man.id)
    fetch(`/add/${man.id}`,{
      method: 'POST',
  })
  .then(response =>  response.json())
  .then(resp => {
    console.log(resp)
  })
    nextmatch(matches[nextelementinarray])
  })
  divimg.append(anotherdiv)
  anketessec.append(root)
}

function sendmess(){
  text = document.querySelector(".textarea")
  fetch(`/newmes/${chatroomid}`, {
    method: 'PUT',
    body: JSON.stringify({
        mes: text.value,
    })
  })
  .then(response => response.json())
  .then(result => {
    text.value ="" 
    console.log(result)
    loadmessages(currentchatid)
  });
}