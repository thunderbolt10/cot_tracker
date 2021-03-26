// Themes begin
//am4core.useTheme(am4themes_animated);
am4core.useTheme(am4themes_amchartsdark);
// Themes end


var chart;

function disposeChart(chartdiv) {
    if (chart) {
      chart.dispose();
      delete chart;
    }
  }

function plot_chart(cot_data, price_data) {

    // Check if the chart instance exists
    disposeChart(chartdiv);

    chart = am4core.create("chartdiv", am4charts.XYChart);
    chart.padding(0, 15, 0, 15);
    chart.colors.step = 3;

    //chart.data = cot_data;
    // the following line makes value axes to be arranged vertically.
    chart.leftAxesContainer.layout = "vertical";

    // uncomment this line if you want to change order of axes
    //chart.bottomAxesContainer.reverseOrder = true;

    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.renderer.ticks.template.length = 8;
    dateAxis.renderer.ticks.template.strokeOpacity = 0.1;
    dateAxis.renderer.grid.template.disabled = true;
    dateAxis.renderer.ticks.template.disabled = false;
    dateAxis.renderer.ticks.template.strokeOpacity = 0.2;
    dateAxis.renderer.minLabelPosition = 0.01;
    dateAxis.renderer.maxLabelPosition = 0.99;
    dateAxis.keepSelection = true;

    dateAxis.groupData = false;
    dateAxis.minZoomCount = 5;
    dateAxis.baseInterval = {
      "timeUnit": "day",
      "count": 1
    };

    dateAxis.tooltipDateFormat = "dd-MM-yyyy";
    
    
    // COT Open Interest chart
    var OIAxis = chart.yAxes.push(new am4charts.ValueAxis());
    OIAxis.tooltip.disabled = true;
    // height of axis
    OIAxis.height = am4core.percent(10);
    OIAxis.zIndex = 2;
    OIAxis.marginTop = 18;
    OIAxis.renderer.baseGrid.disabled = true;
    OIAxis.renderer.inside = false;
    OIAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
    OIAxis.renderer.gridContainer.background.fillOpacity = 0.1;
    OIAxis.renderer.labels.template.verticalCenter = "middle";
    OIAxis.renderer.labels.template.padding(2, 2, 2, 2);
    //valueAxis.renderer.maxLabelPosition = 0.95;
    OIAxis.renderer.fontSize = "0.8em"
    
    var OIseries = chart.series.push(new am4charts.LineSeries());
    OIseries.stroke = am4core.color('#ebf068');
    OIseries.data = cot_data;
    OIseries.dataFields.dateX = "date";
    OIseries.dataFields.valueY = "oi";
    OIseries.yAxes = OIAxis;
    OIseries.fillOpacity = 0.5;
    OIseries.tooltipText = "{name}: {valueY}";
    OIseries.name = "Open Interest";
    OIseries.tooltip.getFillFromObject = false;
    OIseries.tooltip.getStrokeFromObject = true;
    OIseries.tooltip.background.fill = am4core.color('#444');
    OIseries.tooltip.label.fill = am4core.color('#ebf068');
    
    var fillModifier = new am4core.LinearGradientModifier();
    fillModifier.opacities = [0.5, 0];
    fillModifier.offsets = [0, 1];
    fillModifier.gradient.rotation = 90;
    OIseries.segments.template.fillModifier = fillModifier;
      

    // COT MM & PM chart
    var cotAxis = chart.yAxes.push(new am4charts.ValueAxis());
    cotAxis.tooltip.disabled = true;
    // height of axis
    cotAxis.height = am4core.percent(30);
    cotAxis.zIndex = 3;
    cotAxis.min = 0;
    cotAxis.max = 100;
    cotAxis.strictMinMax = true;
    // this makes gap between panels
    cotAxis.marginTop = 30;
    cotAxis.renderer.baseGrid.disabled = true;
    cotAxis.renderer.inside = false;
    cotAxis.renderer.labels.template.verticalCenter = "middle";
    cotAxis.renderer.labels.template.padding(2, 2, 2, 2);
    //valueAxis.renderer.maxLabelPosition = 0.95;
    cotAxis.renderer.fontSize = "0.8em";
    cotAxis.title.text = '%';

    cotAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
    cotAxis.renderer.gridContainer.background.fillOpacity = 0.1;

    var PMSeries = chart.series.push(new am4charts.StepLineSeries());
    //PMSeries.fillOpacity = 1;
    //PMSeries.fill = series1.stroke;
    PMSeries.data = cot_data;
    PMSeries.stroke = am4core.color("#39b2ea");
    PMSeries.dataFields.dateX = "date";
    PMSeries.dataFields.valueY = "pm5";
    PMSeries.yAxis = cotAxis;
    PMSeries.tooltipText = "PM: {valueY.formatNumber('#.#|0')}%";
    PMSeries.name = "PM";
    PMSeries.tooltip.getFillFromObject = false;
    PMSeries.tooltip.getStrokeFromObject = true;
    PMSeries.tooltip.background.fill = am4core.color('#444');
    PMSeries.tooltip.label.fill = am4core.color('#39b2ea');
    
    var MMSeries = chart.series.push(new am4charts.StepLineSeries());
    //MMSeries.fillOpacity = 1;
    //MMSeries.fill = series1.stroke;
    MMSeries.data = cot_data;
    MMSeries.stroke = am4core.color("#99ea39");
    MMSeries.dataFields.dateX = "date";
    MMSeries.dataFields.valueY = "mm5";
    MMSeries.yAxis = cotAxis;
    MMSeries.tooltipText = "MM: {valueY.formatNumber('#.#|0')}%";
    MMSeries.name = "MM";
    MMSeries.tooltip.getFillFromObject = false;
    MMSeries.tooltip.getStrokeFromObject = true;
    MMSeries.tooltip.background.fill = am4core.color('#444');
    MMSeries.tooltip.label.fill = am4core.color('#99ea39');
    
    // Prices chart
    var priceAxis = chart.yAxes.push(new am4charts.ValueAxis());
    priceAxis.tooltip.disabled = true;
    // height of axis
    priceAxis.height = am4core.percent(30);
    priceAxis.zIndex = 1;
    priceAxis.marginTop = 30;
    // this makes gap between panels
    priceAxis.renderer.baseGrid.disabled = true;
    priceAxis.renderer.inside = false;
    priceAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
    priceAxis.renderer.gridContainer.background.fillOpacity = 0.1;
    priceAxis.renderer.labels.template.verticalCenter = "middle";
    priceAxis.renderer.labels.template.padding(2, 2, 2, 2);
    //valueAxis.renderer.maxLabelPosition = 0.95;
    priceAxis.renderer.fontSize = "0.8em";
    priceAxis.title.text = '$';
    /*
    var HLseries = chart.series.push(new am4charts.LineSeries());
    HLseries.data = price_data
    HLseries.dataFields.dateX = "date";
    HLseries.dataFields.openValueY = "high";
    HLseries.dataFields.valueY = "low";
    //HLseries.tooltipText = "open: {openValueY.value} close: {valueY.value}";
    HLseries.fillOpacity = 0.5;
    HLseries.tensionX = 0.8;
    HLseries.yAxis = priceAxis;
    HLseries.name = "Price Range";
    HLseries.strokeOpacity = 0;
    HLseries.fill = am4core.color('#f0b0b0');
    //HLseries.sequencedInterpolation = false;
    //HLseries.defaultState.transitionDuration = 1000;
    */

    var PriceSeries = chart.series.push(new am4charts.LineSeries());
    PriceSeries.data = price_data
    PriceSeries.stroke = am4core.color("#ee4747");
    PriceSeries.dataFields.dateX = "date";
    PriceSeries.dataFields.valueY = "close";
    PriceSeries.yAxis = priceAxis;
    PriceSeries.tooltipText = "Price: {valueY}";
    PriceSeries.name = "Price";
    PriceSeries.tooltip.getFillFromObject = false;
    PriceSeries.tooltip.getStrokeFromObject = true;
    PriceSeries.tooltip.background.fill = am4core.color('#444');
    PriceSeries.tooltip.label.fill = am4core.color('#ee4747');
    PriceSeries.strokeWidth = 2;
    



    var volumeAxis = chart.yAxes.push(new am4charts.ValueAxis());
    volumeAxis.tooltip.disabled = true;
    //volumeAxis.renderer.opposite = true;
    // height of axis
    volumeAxis.height = am4core.percent(12);
    volumeAxis.zIndex = 1
    volumeAxis.marginTop = 30;
    volumeAxis.renderer.baseGrid.disabled = true;
    volumeAxis.renderer.inside = false;
    volumeAxis.renderer.labels.template.verticalCenter = "middle";
    volumeAxis.renderer.labels.template.padding(2, 2, 2, 2);
    //valueAxis.renderer.maxLabelPosition = 0.95;
    volumeAxis.renderer.fontSize = "0.8em"
    volumeAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
    volumeAxis.renderer.gridContainer.background.fillOpacity = 0.1;

    var VolSeries = chart.series.push(new am4charts.ColumnSeries());
    VolSeries.data = price_data
    VolSeries.dataFields.dateX = "date";
    VolSeries.dataFields.valueY = "volume";
    VolSeries.yAxis = volumeAxis;
    VolSeries.tooltipText = "Volume: {valueY.value}";
    VolSeries.name = "Volume";
    VolSeries.stroke = am4core.color("#25aa57");
    VolSeries.fill = am4core.color("#25aa57");
    VolSeries.tooltip.getFillFromObject = false;
    VolSeries.tooltip.getStrokeFromObject = true;
    VolSeries.tooltip.background.fill = am4core.color('#444');
    VolSeries.tooltip.label.fill = am4core.color('#25aa57');
    // volume should be summed
    VolSeries.groupFields.valueY = "sum";
    //VolSeries.defaultState.transitionDuration = 1000;
    //VolSeries.sequencedInterpolation = false;


    var div_height = document.getElementById('chartdiv').clientHeight.toString();
    console.log('div height: ', div_height);

    positions = {
      '720': {
        'oi': 0,
        'pm': 77,
        'price': 271,
        'vol': 467,
      },
      '800': {
        'oi': 0,
        'pm': 88,
        'price': 311,
        'vol': 535,
      }
    }
    var OIlabel = chart.plotContainer.createChild(am4core.Label);
    OIlabel.text = "Open Interest";
    OIlabel.x = 50;
    OIlabel.y = positions[div_height]['oi'];


    var PMlabel = chart.plotContainer.createChild(am4core.Label);
    PMlabel.text = "Dealers and Speculators";
    PMlabel.x = 50;
    PMlabel.y = positions[div_height]['pm'];


    var Pricelabel = chart.plotContainer.createChild(am4core.Label);
    Pricelabel.text = "Price (weekly)";
    Pricelabel.x = 50;
    Pricelabel.y = positions[div_height]['price'];

    
    var Vollabel = chart.plotContainer.createChild(am4core.Label);
    Vollabel.text = "Volume (weekly)";
    Vollabel.x = 50;
    Vollabel.y = positions[div_height]['vol'];

    chart.cursor = new am4charts.XYCursor();

    var scrollbarX = new am4charts.XYChartScrollbar();
    scrollbarX.series.push(PriceSeries);
    scrollbarX.marginBottom = 10;
    
    var sbSeries = scrollbarX.scrollbarChart.series.getIndex(0);
    sbSeries.dataFields.valueYShow = undefined;
    chart.scrollbarX = scrollbarX;
    chart.scrollbarX.parent = chart.bottomAxesContainer;
    
    chart.legend = new am4charts.Legend();
    chart.legend.postion = 'bottom';
    //chart.legend.useDefaultMarker = true;
    
    // Add range selector
    var selector = new am4plugins_rangeSelector.DateAxisRangeSelector();
    selector.container = document.getElementById("controls");
    selector.axis = dateAxis;
    selector.inputDateFormat = "dd-MM-yyyy";

    dateAxis.showOnInit = false;

    chart.events.on("ready", function() {
      var max = dateAxis.max;
      var date1 = new Date(max);
      var date2 = new Date(max);
      console.log('date1: ', date1);
      am4core.time.add(date1, "year", -1);
      console.log('date2: ', date1, date2, max)
      dateAxis.zoomToDates(date1, date2, false, true);
    });
}; // end am4core.ready()




