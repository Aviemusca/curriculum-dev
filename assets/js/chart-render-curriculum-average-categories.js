import ChartRenderBar from './chart-render-bar.js';

export default class ChartRenderCurriculumAverageCategories extends ChartRenderBar {
    constructor(url=null, analysisPk=null, numLOs=null){
        super(url, analysisPk, numLOs);
        this.elementIdRoot = "curriculum-average-categories-chart";
    }
    setChartAttributes(){
        this.chartTitle = "Average categories per LO";
        //this.labelString = "percentage of learning outcomes";
        //this.ticksUnit = "%";
    }
}
