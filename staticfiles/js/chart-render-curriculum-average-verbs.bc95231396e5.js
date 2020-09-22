import ChartRenderBar from './chart-render-bar.js';

export default class ChartRenderCurriculumAverageVerbs extends ChartRenderBar {
    constructor(url=null, analysisPk=null, numLOs=null){
        super(url, analysisPk, numLOs);
        this.elementIdRoot = "curriculum-average-verbs-chart";
    }
    setChartAttributes(){
        this.chartTitle = "Average verb hits per LO";
        //this.labelString = "percentage of learning outcomes";
        //this.ticksUnit = "%";
    }
}
