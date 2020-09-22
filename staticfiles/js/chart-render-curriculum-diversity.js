import ChartRenderStackedBar from './chart-render-stacked-bar.js';

export default class ChartRenderCurriculumDiversity extends ChartRenderStackedBar {
    constructor(url=null, analysisPk=null, numLOs=null){
        super(url, analysisPk, numLOs);
        this.elementIdRoot = "curriculum-diversity-chart";
    }
    setChartAttributes(){
        this.chartTitle = "LO Occurrences vs Number of Categories";
        this.labelString = "percentage of learning outcomes";
        this.ticksUnit = "%";
    }
}
