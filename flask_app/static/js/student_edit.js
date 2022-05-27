
// var editEmail = document.querySelector('#edit_email')
// editEmail.addEventListener('click', function(){
//     let parent = this.parentElement
//     parent.classList.add('hidden')
//     parent.nextElementSibling.classList.remove('hidden')
// })

// var emailInput = document.querySelector('#email_input')
// emailInput.addEventListener('focusout', async function(){
//     let email = this.value
//     let parent = this.parentElement
//     parent.classList.add('hidden')
//     parent.previousElementSibling.classList.remove('hidden')
//     let id = this.getAttribute('user_id')

//     let form = new FormData()
//     form.append('email', email)

//     let url = `/api/user/${id}/update`
//     resp = await updateField(url, form)

//     if (resp.status == 200){
//         parent.previousElementSibling.children[0].textContent = email
//     }
// })


