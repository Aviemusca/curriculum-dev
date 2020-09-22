import ChartRender from './chart-render.js';

export default class ChartRenderTaxonomyVerbNumbers extends ChartRender {
    constructor(url=null, analysisPk=null, numLOs=null){
        super(url, analysisPk);
        this.elementIdRoot = 'taxonomy-verb-number-chart';

        // Data Attributes
    }

    formatDataChart(){
        /* Allows fetchFormatRender method to reside in  parent class */
        this.createBarChartDataSet();
    }
    renderUpdatedColours(colours){
        this.colours = colours;
        this.createBarChartDataSet();
        this.renderChart();
    }
    createBarChartDataSet(){
        /* Generates bar chart data set for chart js */
        const categoryColors = [];
        const borderColors = [];

        this.barChartDataSet = [];
        this.barChartDataSet.push({
            data: this.data,
            borderWidth: 1,
            backgroundColor: categoryColors,
            borderColor: borderColors,
            });
    }

    setChartAttributes(){
        this.chartTitle = "Number of Verbs vs Category";
        this.labelString = "number of verbs";
    }
    renderChart(){
        /* Render the chart with chart.js */
        const ctx = document.getElementById(`${this.elementIdRoot}-${this.analysisPk}`).getContext('2d');
        Chart.defaults.global.defaultFontColor = '#444444';
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: this.labels,
                datasets: this.barChartDataSet,
            },
            options: {
                title: {
                    text: this.chartTitle,
                    display: true
                },
                scales: {
                    xAxes:[{
                        stacked: true,
                    }],
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: this.labelString,
                        },

                    }]
                },
                legend: {
                    display: false,
                },

            }
        });
    }
}
