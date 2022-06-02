var allCheckBtns = document.querySelectorAll('.student_checkbox')
var massDeleteBtn = document.querySelector('.mass_delete_btn')
var selectAllBtn = document.querySelector('.select_all_btn')
massUpdateList = []

for (const box of allCheckBtns) {
    box.addEventListener('change', function () {
        addRemoveToList(this)
    })
}

massDeleteBtn.addEventListener('click', async function () {
    let form = new FormData()
    form.append('list', JSON.stringify(massUpdateList))

    resp = await fetch('/api/student/mass/delete', {
        method: 'post',
        body: form
    })
    for (const obj of massUpdateList) {
        obj.element.parentElement.parentElement.remove()
    }
    clearList()
})


function addRemoveToList(el) {
    let student_id = el.getAttribute('student_id')
    let user_id = el.getAttribute('user_id')

    let foundIndex = massUpdateList.findIndex((element) => element.student_id === student_id)
    if (foundIndex !== -1) {
        massUpdateList.splice(foundIndex, 1)
    } else {
        massUpdateList.push({
            student_id: student_id,
            user_id: user_id,
            element: el
        })
    }
    updateButtons()
}

function addToList(el) {
    let student_id = el.getAttribute('student_id')
    let user_id = el.getAttribute('user_id')

    let foundIndex = massUpdateList.findIndex((element) => element.student_id === student_id)
    if (foundIndex === -1) {
        massUpdateList.push({
            student_id: student_id,
            user_id: user_id,
            element: el
        })
    }
    updateButtons()
}

function clearList(){
    massUpdateList = []
    updateButtons()
}

function updateButtons() {
    if (massUpdateList.length > 0) {
        massDeleteBtn.classList.remove('disabled')
    } else {
        massDeleteBtn.classList.add('disabled')
    }
}

selectAllBtn.addEventListener('click', function () {
    console.log(massUpdateList.length); 
    console.log(allCheckBtns.length); 
    if (massUpdateList.length != allCheckBtns.length){
        for (const btn of allCheckBtns) {
            addToList(btn)
            btn.checked = true
        }
    } else {
        for (const btn of allCheckBtns) {
            btn.checked = false
        }
        clearList()
    }
})