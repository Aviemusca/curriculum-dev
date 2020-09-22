import ChartRenderStackedBar from './chart-render-stacked-bar.js';

export default class ChartRenderCurriculumAnalyis extends ChartRenderStackedBar {
    constructor(url=null, analysisPk=null, numLOs=null){
        super(url, analysisPk, numLOs);
        this.elementIdRoot = "curriculum-analysis-chart";
    }
    setChartAttributes(){
        this.chartTitle = "LO Occurrences vs Category";
        this.labelString = "percentage of learning outcomes";
        this.ticksUnit = "%";
    }
}
