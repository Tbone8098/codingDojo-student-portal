
var isCurrentBox = document.querySelectorAll('.is_current')
for (const box of isCurrentBox) {
    box.addEventListener('change', updateCurrent(box))
}

function updateCurrent(el) {
    console.log(el);
    let status = el.getAttribute('status')
    let id = el.parentElement.parentElement.getAttribute('cohort_id')
    console.log(status);

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
            if (data.msg === 'success') {
                if (status) {
                    el.parentElement.innerHTML = `
                    <input type="checkbox" name="is_current" class="is_current" status="${status}" checked> Yes
                    `
                } else {
                    el.parentElement.innerHTML = `
                    <input type="checkbox" name="is_current" class="is_current" status="${status}"> No
                    `
                }
            }
        })
}