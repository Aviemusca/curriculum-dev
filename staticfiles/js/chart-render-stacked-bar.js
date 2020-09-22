import ChartRender from './chart-render.js';

export default class ChartRenderStackedBar extends ChartRender {
    constructor(url=null, analysisPk=null, numLOs=null){
        super(url, analysisPk);
        this.numLOs=numLOs;

        // Data Attributes
        this.yNumbers = [];
        this.yPercentages = [];
    }
    createYpercentages(){
        /* maps LO numbers to LO percentages from total number of LOs */
        this.yPercentages = this.yNumbers.map(x => (x / this.numLOs * 100).toFixed(2));
    }
    formatDataChart(){
        /* Allows fetchFormatRender method to reside in  parent class */
        this.createBarChartDataSets();
    }
    renderUpdatedColours(colours){
        this.colours = colours;
        this.createBarChartDataSets();
        this.renderChart();
    }
    createBarChartDataSets(){
        /* Generates bar chart data sets for chart js */
        const strandColors = this.colours.map(colour => this.hexToRgbA(colour, 0.6));
        const borderColors = this.colours.map(colour => this.hexToRgbA(colour, 1));

        this.barChartDataSets = [];
        this.data.forEach((strand, index) => {
            this.yNumbers = strand;
            this.createYpercentages();
            this.barChartDataSets.push({
                data: this.yPercentages,
                borderWidth: 1,
                backgroundColor: strandColors[index],
                borderColor: borderColors[index],
            })
        });
    }
    renderChart(){
        /* Render the chart with chart.js */
        const ctx = document.getElementById(`${this.elementIdRoot}-${this.analysisPk}`).getContext('2d');
        Chart.defaults.global.defaultFontColor = '#444444';
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: this.labels,
                datasets: this.barChartDataSets,
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
                        stacked: true,
                        scaleLabel: {
                            display: true,
                            labelString: this.labelString,
                        },
                        ticks: {
                            beginAtZero: true,
                            callback: value => value + this.ticksUnit,
                        }
                    }]
                },
                legend: {
                    display: false,
                },
            }
        });
    }
}

