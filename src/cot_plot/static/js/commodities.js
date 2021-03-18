// Themes begin
am4core.useTheme(am4themes_animated);
am4core.useTheme(am4themes_amchartsdark);
// Themes end


var chart;

function disposeChart(chartdiv) {
    if (chart) {
      chart.dispose();
      delete chart;
    }
  }

function plot_chart(data) {

    // Check if the chart instance exists
    disposeChart(chartdiv);

    chart = am4core.create("chartdiv", am4charts.XYChart);
    chart.padding(0, 15, 0, 15);
    chart.colors.step = 3;

    chart.data = data;
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

    dateAxis.groupData = true;
    dateAxis.minZoomCount = 5;

    // these two lines makes the axis to be initially zoomed-in
    // dateAxis.start = 0.7;
    // dateAxis.keepSelection = true;

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.zIndex = 1;
    valueAxis.renderer.baseGrid.disabled = true;
    // height of axis
    valueAxis.height = am4core.percent(50);

    valueAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
    valueAxis.renderer.gridContainer.background.fillOpacity = 0.05;
    valueAxis.renderer.inside = false;
    valueAxis.renderer.labels.template.verticalCenter = "middle";
    valueAxis.renderer.labels.template.padding(2, 2, 2, 2);

    //valueAxis.renderer.maxLabelPosition = 0.95;
    valueAxis.renderer.fontSize = "0.8em"

    var OIseries = chart.series.push(new am4charts.LineSeries());
    OIseries.stroke = am4core.color('#ebf068');
    OIseries.dataFields.dateX = "date";
    OIseries.dataFields.valueY = "oi";
    OIseries.fillOpacity = 0.5;
    //series1.dataFields.valueYShow = "changePercent";
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

    
    var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis2.tooltip.disabled = true;
    // height of axis
    valueAxis2.height = am4core.percent(50);
    valueAxis2.zIndex = 3;
    valueAxis2.min = 0;
    valueAxis2.max = 100;
    valueAxis2.strictMinMax = true;
    // this makes gap between panels
    valueAxis2.marginTop = 30;
    valueAxis2.renderer.baseGrid.disabled = true;
    valueAxis2.renderer.inside = false;
    valueAxis2.renderer.labels.template.verticalCenter = "middle";
    valueAxis2.renderer.labels.template.padding(2, 2, 2, 2);
    //valueAxis.renderer.maxLabelPosition = 0.95;
    valueAxis2.renderer.fontSize = "0.8em";
    valueAxis2.title.text = '%';

    valueAxis2.renderer.gridContainer.background.fill = am4core.color("#000000");
    valueAxis2.renderer.gridContainer.background.fillOpacity = 0.05;

    var PMSeries = chart.series.push(new am4charts.StepLineSeries());
    //PMSeries.fillOpacity = 1;
    //PMSeries.fill = series1.stroke;
    PMSeries.stroke = am4core.color("#39b2ea");
    PMSeries.dataFields.dateX = "date";
    PMSeries.dataFields.valueY = "pm5";
    PMSeries.yAxis = valueAxis2;
    PMSeries.tooltipText = "PM: {valueY.formatNumber('#.#|0')}%";
    PMSeries.name = "PM";

    PMSeries.tooltip.getFillFromObject = false;
    PMSeries.tooltip.getStrokeFromObject = true;
    PMSeries.tooltip.background.fill = am4core.color('#444');
    PMSeries.tooltip.label.fill = am4core.color('#39b2ea');
    
    var MMSeries = chart.series.push(new am4charts.StepLineSeries());
    //MMSeries.fillOpacity = 1;
    //MMSeries.fill = series1.stroke;
    MMSeries.stroke = am4core.color("#99ea39");
    MMSeries.dataFields.dateX = "date";
    MMSeries.dataFields.valueY = "mm5";
    MMSeries.yAxis = valueAxis2;
    MMSeries.tooltipText = "MM: {valueY.formatNumber('#.#|0')}%";
    MMSeries.name = "MM";
    chart.cursor = new am4charts.XYCursor();

    
    MMSeries.tooltip.getFillFromObject = false;
    MMSeries.tooltip.getStrokeFromObject = true;
    MMSeries.tooltip.background.fill = am4core.color('#444');
    MMSeries.tooltip.label.fill = am4core.color('#99ea39');

    var scrollbarX = new am4charts.XYChartScrollbar();
    scrollbarX.series.push(OIseries);
    scrollbarX.marginBottom = 20;
    var sbSeries = scrollbarX.scrollbarChart.series.getIndex(0);
    sbSeries.dataFields.valueYShow = undefined;
    chart.scrollbarX = scrollbarX;

    chart.legend = new am4charts.Legend();
    chart.legend.postion = 'bottom';
    //chart.legend.useDefaultMarker = true;
    
    // Add range selector
    var selector = new am4plugins_rangeSelector.DateAxisRangeSelector();
    selector.container = document.getElementById("controls");
    selector.axis = dateAxis;

}; // end am4core.ready()

