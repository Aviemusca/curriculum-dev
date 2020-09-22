export default class ChartRender {
    constructor(url=null, colours=null, chartTitle=null, analysisPk=null, chartLabelString=null){
        this.dataUrl = url;
        this.analysisPk = analysisPk; // The primary key of whichever analysis is being charted
        this.colours = colours;

        // Chart attributes
        this.chartTitle = chartTitle;
        this.chartLabelString = chartLabelString;
    }

    setDataUrl(chartDivBox){
        /* grabs the url containing the json data */
        this.dataUrl = chartDivBox.getAttribute('data-url');
    }

    extractUrlData(data){
        /* Extracts the data and labels for chart rendering from json parsed url data */
        this.data = data.data;
        this.analysisPk = data.analysisPk;
        this.labels = data.labels;
        if (this.colours == null) // When the user has not changed any colour
            this.colours = data.colours;
        if (data.numLOs)
            this.numLOs = data.numLOs;
    }
    fetchFormatRender(){
    /* Fetch the json url data, format the data and plot the chart */
        fetch(this.dataUrl)
            .then(response => response.json())
            .then(data => {
                this.extractUrlData(data);
                this.formatDataChart();     // Each subclass has their own version of this method
                this.renderChart();
            })
            .catch( error => console.log(`Error: ${error.message}`));
    }
    hexToRgbA(hex, alpha){
    let c;
    if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
        c= hex.substring(1).split('');
        if(c.length== 3){
            c= [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c= '0x'+c.join('');
        return 'rgba('+[(c>>16)&255, (c>>8)&255, c&255].join(',')+`,${alpha})`;
    } else if(/^([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
        c= hex.split('');
        if(c.length== 3){
            c= [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c= '0x'+c.join('');
        return 'rgba('+[(c>>16)&255, (c>>8)&255, c&255].join(',')+`,${alpha})`;
    }
    throw new Error('Bad Hex');
}
}
