
var isCurrentBox = document.querySelectorAll('.is_current')
for (const box of isCurrentBox) {
    box.addEventListener('change', function(){
        return updateCurrent(box)
    })
}

function updateCurrent(el) {
    let status = el.getAttribute('status')
    let id = el.parentElement.parentElement.getAttribute('cohort_id')
    
    if (status == 1) {
        el.setAttribute('status', '0')
        el.parentElement.children[1].textContent = "No"
        
    } else {
        el.setAttribute('status', '1')
        el.parentElement.children[1].textContent = "Yes"
    }

    form = new FormData()
    if (status == 1) status = 0
    else status = 1
    form.append('is_current', status)

    fetch(`api/cohort/${id}/update`, {
        method: 'post',
        body: form
    })
        .then(resp => resp.json())
        .then(data => {
            console.log(data);
            if (data.msg != 'success') {
                if (status) {
                    console.log("test1");
                    el.setAttribute('status', 1)
                    el.parentElement.children[1].textContent = "Yes"
                    
                } else {
                    console.log("test2");
                    el.setAttribute('status', 0)
                    el.parentElement.children[1].textContent = "No"
                }
            }
        })
}