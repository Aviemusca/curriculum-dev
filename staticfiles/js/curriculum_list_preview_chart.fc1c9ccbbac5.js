import ChartRenderCurriculumAnalysis from './chart-render-curriculum-analysis.js';

function hitCountChartRender(strandColours=null){
    /* Script for rendering the category hit count charts of all the curriculum analyses.
     * The first time running the script, the stand colours are grabbed from the database.
     * Subsequent runnings of the script are due to user changing colour and these are
     * provided as a parameter array */

    // Get all the elements where the charts will be rendered to (for each analysis)
    let chartBoxes = document.querySelectorAll('.list-chart-box');

    // Create an array for the ChartRender objects
    let chartRenders = [];
    let currentChartRender;

    Array.from(chartBoxes).forEach((box, index, boxes) => {
        chartRenders.push(new ChartRenderCurriculumAnalysis());
        currentChartRender = chartRenders[index];
        currentChartRender.setDataUrl(box);
        currentChartRender.setChartAttributes();
        currentChartRender.chartTitle=""
        currentChartRender.fetchFormatRender();
    })
};
hitCountChartRender();
