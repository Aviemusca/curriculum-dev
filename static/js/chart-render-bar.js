import ChartRender from './chart-render.js';

export default class ChartRenderBar extends ChartRender {
    constructor(url=null, analysisPk=null, numLOs=null){
        super(url, analysisPk);

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
        const strandColors = this.colours.map(colour => this.hexToRgbA(colour, 0.7));
        const borderColors = this.colours.map(colour => this.hexToRgbA(colour, 1));

        this.barChartDataSet = [];
        this.barChartDataSet.push({
            data: this.data,
            borderWidth: 1,
            backgroundColor: strandColors,
            borderColor: borderColors,
            });
    }

    renderChart(){
        /* Render the chart with chart.js */
        const ctx = document.getElementById(`${this.elementIdRoot}-${this.analysisPk}`).getContext('2d');
        Chart.defaults.global.defaultFontColor = '#444444';
        const chart = new Chart(ctx, {
            type: 'horizontalBar',
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

