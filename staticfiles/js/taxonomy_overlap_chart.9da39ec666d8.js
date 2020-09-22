import ChartRenderTaxonomyOverlap from './chart-render-taxonomy-overlap.js';

function overlapChartRender(categoryColours=null){
    /* Script for rendering the overlap chart of a taxonomy
     * */

    // Get the div element where the chart will be rendered to
    const chartBox = document.getElementById('taxonomy-overlap-chart');
    const chartRender = new ChartRenderTaxonomyOverlap();
    chartRender.setDataUrl(chartBox);
    console.log(chartRender)
    chartRender.fetchFormatRender();
};
overlapChartRender();
