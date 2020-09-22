export default class ProgressBar {
    contructor(url=null, analysisPk=null, totalTasks){
        this.domElement =
        this.dataUrl = url;
        this.analyisPk = analysisPk; // The primary key of the analysis in process
        this.percentComplete = percentComplete; // The percentage completion of the back-end tasks
    }

    setDataUrl(progressBarElement){
        /* grabs the url containing the json data */
        this.dataUrl = progressBarElement.getAttribute('data-url');
    }
    extractUrlData(data){
        /* Extracts the data for progress rendering from the json parsed url data */
        this.percentComplete = data.percentComplete;
    }
    render(domElement){
        /* Fetch the json url data, extract the data and render progress bar */
        console.log(this.dataUrl)
        fetch(this.dataUrl)
            .then(response => response.json())
            .then(data => {
                this.extractUrlData(data);
                this.setPercentageComplete(domElement);
        })
        .catch( error => console.log(`Error: ${error.message}`));
    }
    setPercentageComplete(domElement){
        console.log(domElement)
        domElement.style.setProperty('--width', this.percentComplete);
    }
}

