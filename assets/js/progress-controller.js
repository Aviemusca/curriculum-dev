export default class ProgressController{
    contructor(dataUrl=null, successUrl=null, analysisPk=null, taskStatus=null){
        this.dataUrl = url;
        this.successUrl = successUrl;
        this.analyisPk = analysisPk; // The primary key of the analysis in process
        this.taskStatus = taskStatus; // The percentage completion of the back-end tasks
    }

    getDataUrl(element){
        /* grabs the url containing the json data from a DOM element */
        this.dataUrl = element.getAttribute('data-url');
    }
    getSuccessUrl(element){
        /* grabs the success url to redirect to */
        this.successUrl = element.getAttribute('success-url');
    }
    getTaskStatus(data){
        /* Gets the status of the task from the json parsed url data */
        this.taskStatus = data.taskStatus;
    }
    updateView(heading){
        /* Fetch the json url data, get the task status and updates the view accordingly */
        fetch(this.dataUrl)
            .then(response => response.json())
            .then(data => {
                this.getTaskStatus(data);
                return this.taskStatus;
            })
            .then(status => {
                if (status === 'SUCCESS'){
                    setTimeout(() => {this.renderSuccessView(heading);}, 2000);
                }
                else if (status === 'PENDING')
                    this.renderPendingView(heading);
            })
            .catch( error => console.log(`Error: ${error.message}`));
    }

    renderInitialView(heading){
        /* Injects an initial analysis successfully created message into the DOM */

        // Create a new success bootstrap alert msg
        const successMsg = document.createElement('div');
        successMsg.classList.add('alert', 'alert-success');
        successMsg.textContent = "Curriculum analysis created successfully!"

        // Append the success message to the heading
        heading.appendChild(successMsg)
    }

    renderPendingView(heading){
        /* Removes the initial success message and replaces it with an info alert msg */
        const successMsg = document.querySelector('div.alert.alert-success');
        if (successMsg){

            // Create a new info bootstrap alert msg
            const infoMsg = document.createElement('div');
            infoMsg.classList.add('alert', 'alert-info');
            infoMsg.textContent = "Currently processing... We will provide a link with the results shortly. "

            // Remove the original success message
            successMsg.remove()

            // Append the info msg to the heading
            heading.appendChild(infoMsg)
        }
    }
    renderSuccessView(heading){
        /* Removes the info message and replaces it with a success alert msg
         * and a link to the analysis */
        const infoMsg = document.querySelector('div.alert.alert-info');
        if (infoMsg){

            // Create a new success bootstrap alert msg
            const successMsg = document.createElement('div');
            successMsg.classList.add('alert', 'alert-success');
            successMsg.textContent = "Analysis finished successfully!"

            // Remove the original info message
            infoMsg.remove()

            // Append the info msg to the parent div
            heading.appendChild(successMsg)

            // Inject a link back to the curriculum detail page

            // Get the url from the heading
            this.getSuccessUrl(heading);
            console.log(this.successUrl)
            // Create a new anchor tag with the link
            const anchor = document.createElement('a');
            anchor.setAttribute('href', this.successUrl);
            anchor.textContent = 'See new analysis'
            // Wrap anchor tag in a container div
            const container = document.createElement('div')
            container.classList.add('container')
            container.appendChild(anchor)
            // Append to the parent element of the heading
            heading.parentElement.appendChild(container)
        }
    }
}

