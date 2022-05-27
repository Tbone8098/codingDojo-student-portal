var apiInputs = document.querySelectorAll('.api-input')

for (const item of apiInputs) {
    item.addEventListener('focusout', async function(){
        let url = this.getAttribute('url')
        let info = this.value
        let name = this.name
        
        let form = new FormData()
        form.append(name, info)
        
        results = await updateField(url, form)
        
        // errors
        if (results.hasOwnProperty('errors')){
            let parent = this.parentElement
            let data = results.errors
            for (const error in data) {
                parent.innerHTML += `
                <span class="alert bg-my-danger text-white">${data[error]}</span>
                `
            }

        }
    })
}

async function updateField(url, formData) {
    let resp = await fetch(url, {
        method: 'post',
        body: formData
    })
    return await resp.json()
}