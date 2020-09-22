import ChartRenderCurriculumDiversity from './chart-render-curriculum-diversity.js';

function diversityChartRender(strandColours=null){
    /* Script for rendering the category diversity charts of all the curriculum analyses.
     * The first time running the script, the stand colours are grabbed from the database.
     * Subsequent runnings of the script are due to user changing colour and these are
     * provided as a parameter array */

    // Get all the elements where the charts will be rendered to (for each analysis)
    let chartBoxes = document.querySelectorAll('.analysis-grid-diversity-chart');

    // Create an array for the ChartRender objects
    let chartRenders = [];
    let currentChartRender;
    // Loop over each the analysis boxes
    Array.from(chartBoxes).forEach((box, index, boxes) => {
        chartRenders.push(new ChartRenderCurriculumDiversity());
        currentChartRender = chartRenders[index];
        currentChartRender.setDataUrl(box);
        currentChartRender.setChartAttributes();
        if (strandColours !== null) // Means the chart is being re-rendered due to user changing colour
            currentChartRender.colours = strandColours;
        currentChartRender.fetchFormatRender();
    })
};
diversityChartRender();

export default diversityChartRender;

