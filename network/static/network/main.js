console.log("inworking")
const thisForm = document.querySelector("form12")
function edit(id){
    const thisForm = document.querySelector(`.form${id}`)
    const thisBtn = document.querySelector(`.btn${id}`)
    const thisTextArea = document.querySelector(`.textarea${id}`)
    const thisContent = document.querySelector(`.content${id}`)
    thisTextArea.textContent = thisContent.innerText
    thisForm.style.display = 'block';
    thisBtn.style.display = 'none';
}

function save(id){
    const thisTextAreaContent = document.querySelector(`.textarea${id}`)
    const thisForm = document.querySelector(`.form${id}`)
    const thisBtn = document.querySelector(`.btn${id}`)
    const thisContent = document.querySelector(`.content${id}`)
    console.log(thisTextAreaContent.value)  
    console.log(JSON.stringify({
                      text: thisTextAreaContent.value
                  }))
    fetch(`/Change/${id}`, {
              method: 'PUT',
              body: JSON.stringify({
                 text: thisTextAreaContent.value
              })
            })
            // .then(response => response.json())
            // .then(result => {
            //     console.log(result);
            // });

    thisContent.innerText = thisTextAreaContent.value
    thisForm.style.display = 'none';
    thisBtn.style.display = 'block';
}

function like(id){
    const farbe = document.querySelector(`.img${id}`)
    let span = document.querySelector(`.likes-count${id}`)
    fetch(`/Like/${id}`, {
        method: 'PUT',
      })
      .then(response => response.json())
            .then(result => {
                console.log(result);
                 farbe.style.color = result.boolean? "red": "black"
                 result.boolean? span.innerHTML++: span.innerHTML--
            });
}

function cloz(id){
    const thisForm = document.querySelector(`.form${id}`)
    const thisBtn = document.querySelector(`.btn${id}`)
    thisForm.style.display = 'none';
    thisBtn.style.display = 'block';
    console.log('11')
}

function toggleFollow(id){
    const btn = document.querySelector(`#btn${id}`)
    console.log(id)
    fetch(`/Follow/${id}`, {
        method: 'PUT',
      })
      .then(response => response.json())
            .then(result => {
                console.log(btn)
                if (result.boolean ===true){
                    btn.innerHTML = "follow"
                    btn.classList.remove( "btn-outline-danger")
                    btn.classList.add("btn-outline-success")
                }
                else{
                    btn.innerHTML = "unfollow"
                    btn.classList.remove("btn-outline-success")
                    btn.classList.add( "btn-outline-danger")
                }
                // result.boolean? btn.classList.add("btn","btn-outline-success"): btn.classList.add("btn", "btn-outline-danger")
            });
}
