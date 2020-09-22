import ProgressBar from './progress-bar.js';

(function(){
    /* Script which injects a progress bar into the DOM when a curriculum analysis is in process */
    const progressBox = document.querySelectorAll('.progress-bar')[0];
    const dataUrl = progressBox.getAttribute('data-url');
    const progressBar = new ProgressBar();
    progressBar.setDataUrl(progressBox);
    setInterval(() => {
        progressBar.render(progressBox);
    }, 1000)

})();

