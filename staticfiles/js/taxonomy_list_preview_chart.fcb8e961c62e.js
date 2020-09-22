import ChartRenderTaxonomyVerbNumbers from './chart-render-taxonomy-verb-numbers.js';

function verbNumberChartRender(categoryColours=null){
    /* Script for rendering the category verb number charts of all the taxonomies.
     * */

    // Get all the elements where the charts will be rendered to (for each analysis)
    let chartBoxes = document.querySelectorAll('.list-chart-box');

    // Create an array for the ChartRender objects
    let chartRenders = [];
    let currentChartRender;

    Array.from(chartBoxes).forEach((box, index, boxes) => {
        chartRenders.push(new ChartRenderTaxonomyVerbNumbers());
        currentChartRender = chartRenders[index];
        currentChartRender.setDataUrl(box);
        currentChartRender.setChartAttributes();
        currentChartRender.chartTitle=""
        console.log(currentChartRender)
        currentChartRender.fetchFormatRender();
    })
};
verbNumberChartRender();
