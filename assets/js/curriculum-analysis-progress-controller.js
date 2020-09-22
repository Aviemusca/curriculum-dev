import ProgressController from './progress-controller.js';

(function(){
    /* Script which manipulates the DOM to show the progress of the analysis to the user */

    // Get the heading element containing the data-url, which we will also be appending elements to
    const heading = document.getElementById('analysis-progress-heading');

    // The progress controller fetches analysis task info and renders appropriate view
    const progressController = new ProgressController();

    // Get the data-url for the controller from the heading element
    progressController.getDataUrl(heading);

    // Render the initial success view
    progressController.renderInitialView(heading);

    // Update the view periodically
    setInterval(() => {
        progressController.updateView(heading);
    }, 100)
})();
