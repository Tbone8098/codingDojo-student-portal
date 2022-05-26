
var editEmail = document.querySelector('#edit_email')
editEmail.addEventListener('click', function(){
    let parent = this.parentElement
    parent.classList.add('hidden')
    parent.nextElementSibling.classList.remove('hidden')
})