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
  chart.padding(0, 14, 14, 14);
  chart.colors.step = 3;

  chart.leftAxesContainer.layout = "vertical";

  var dateAxis = chart.xAxes.push(new am4charts.DateAxis());  
  dateAxis.renderer.labels.template.fill = am4core.color("#c7c7c7");
  dateAxis.renderer.grid.template.location = 0;
  dateAxis.renderer.ticks.template.length = 8;
  dateAxis.renderer.ticks.template.strokeOpacity = 0.1;
  dateAxis.renderer.grid.template.disabled = true;
  dateAxis.renderer.ticks.template.disabled = false;
  dateAxis.renderer.ticks.template.strokeOpacity = 0.2;
  dateAxis.renderer.minLabelPosition = 0.01;
  dateAxis.renderer.maxLabelPosition = 0.99;
  dateAxis.keepSelection = true;
  dateAxis.tooltipDateFormat = "dd-MM-yyyy";
  dateAxis.minZoomCount = 5;
  dateAxis.baseInterval = {
    "timeUnit": "day",
    "count": 1
  };

  
  var fillModifier = new am4core.LinearGradientModifier();
  fillModifier.opacities = [0.4, 0];
  fillModifier.offsets = [0, 1];
  fillModifier.gradient.rotation = 90;
  
  // Prices chart
  /*
  var priceAxis = chart.yAxes.push(new am4charts.ValueAxis());
  priceAxis.tooltip.disabled = true;
  // height of axis
  priceAxis.height = am4core.percent(30);
  priceAxis.zIndex = 1;
  priceAxis.marginTop = 20;
  // this makes gap between panels
  priceAxis.renderer.baseGrid.disabled = true;
  priceAxis.renderer.inside = false;
  priceAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
  priceAxis.renderer.gridContainer.background.fillOpacity = 0.2;
  priceAxis.renderer.labels.template.verticalCenter = "middle";
  priceAxis.renderer.labels.template.padding(2, 2, 2, 2);
  priceAxis.renderer.labels.template.fill = am4core.color("#c7c7c7");
  //valueAxis.renderer.maxLabelPosition = 0.95;
  priceAxis.renderer.fontSize = "0.8em";
  priceAxis.title.text = '$';
  priceAxis.title.fill = am4core.color("#c7c7c7");
  
  var PriceSeries = chart.series.push(new am4charts.LineSeries());
  PriceSeries.data = price_data
  PriceSeries.stroke = am4core.color("#ee4747");
  PriceSeries.fill = am4core.color("#ee4747");
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
  PriceSeries.fillOpacity = 0.9;  
  PriceSeries.segments.template.fillModifier = fillModifier;

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
  volumeAxis.renderer.gridContainer.background.fillOpacity = 0.2;
  volumeAxis.renderer.labels.template.fill = am4core.color("#c7c7c7");

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
  */
  // COT MM & PM chart
  var cotAxis = chart.yAxes.push(new am4charts.ValueAxis());
  cotAxis.tooltip.disabled = true;
  // height of axis
  cotAxis.height = am4core.percent(70);
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
  cotAxis.title.fill = am4core.color("#c7c7c7");
  cotAxis.renderer.labels.template.fill = am4core.color("#c7c7c7");
  cotAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
  cotAxis.renderer.gridContainer.background.fillOpacity = 0.2;

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


  // Open Interest chart
  var OIAxis = chart.yAxes.push(new am4charts.ValueAxis());
  OIAxis.tooltip.disabled = true;
  OIAxis.height = am4core.percent(20);
  OIAxis.zIndex = 1;
  OIAxis.marginTop = 30;
  OIAxis.renderer.baseGrid.disabled = true;
  OIAxis.renderer.inside = false;
  OIAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
  OIAxis.renderer.gridContainer.background.fillOpacity = 0.2;
  OIAxis.renderer.labels.template.verticalCenter = "middle";
  OIAxis.renderer.labels.template.padding(2, 2, 2, 2);
  OIAxis.renderer.fontSize = "0.8em";
  OIAxis.title.text = '$';
  OIAxis.title.fill = am4core.color("#c7c7c7");
  OIAxis.renderer.labels.template.fill = am4core.color("#c7c7c7");
  
  var OISeries = chart.series.push(new am4charts.LineSeries());
  OISeries.data = cot_data
  OISeries.stroke = am4core.color("#ebf068");
  OISeries.fill = am4core.color("#ebf068");
  OISeries.dataFields.dateX = "date";
  OISeries.dataFields.valueY = "oi";
  OISeries.yAxis = OIAxis;
  OISeries.tooltipText = "{name}: {valueY}";
  OISeries.name = "Open Interest";
  OISeries.tooltip.getFillFromObject = false;
  OISeries.tooltip.getStrokeFromObject = true;
  OISeries.tooltip.background.fill = am4core.color('#444');
  OISeries.tooltip.label.fill = am4core.color('#ebf068');
  OISeries.strokeWidth = 2;
  OISeries.fillOpacity = 0.9;  
  OISeries.segments.template.fillModifier = fillModifier;
    
  
  var div_height = document.getElementById('chartdiv').clientHeight.toString();
    console.log('div height: ', div_height);

  var div_width = (document.getElementById('chartdiv').clientWidth / 2 ).toString();

  positions = {
    
      'pm': 2,
      'oi': Math.round(div_height * 0.685),
    /*
    '720': {
      'price': 2,
      'vol': 210,
      'pm': 290,
      'so': 350,
      'oi': 486,
    },
    '780': {
      'price': 2,
      'vol': 230,
      'pm': 317,
      'so': 460,
      'oi': 535,
    }
    */
  }
  
  /*
  var Pricelabel = chart.plotContainer.createChild(am4core.Label);
  Pricelabel.fill = am4core.color("#c7c7c7");
  Pricelabel.text = "Price";
  Pricelabel.x = div_width - 60;
  Pricelabel.y = positions[div_height]['price'];

  
  var Vollabel = chart.plotContainer.createChild(am4core.Label);
  Vollabel.fill = am4core.color("#c7c7c7");
  Vollabel.text = "Volume";
  Vollabel.x = div_width - 70;
  Vollabel.y = positions[div_height]['vol'];  
  */
  var PMlabel = chart.plotContainer.createChild(am4core.Label);
  PMlabel.fill = am4core.color("#c7c7c7");
  PMlabel.text = "Dealers and Speculators";
  PMlabel.x = div_width - 120;
  PMlabel.y = positions['pm'];
  
  var OIlabel = chart.plotContainer.createChild(am4core.Label);
  OIlabel.fill = am4core.color("#c7c7c7");
  OIlabel.text = "Open Interest";
  OIlabel.x = div_width - 87;
  OIlabel.y = positions['oi'];
  

  chart.cursor = new am4charts.XYCursor();
  
  var scrollbarX = new am4charts.XYChartScrollbar();
  scrollbarX.series.push(PMSeries);
  //scrollbarX.marginBottom = 10;

  var sbSeries = scrollbarX.scrollbarChart.series.getIndex(0);
  sbSeries.dataFields.valueYShow = undefined;
  chart.scrollbarX = scrollbarX;
  chart.scrollbarX.parent = chart.bottomAxesContainer;
  chart.scrollbarX.minHeight = 40;

  //chart.legend = new am4charts.Legend();
  //chart.legend.postion = 'bottom';
  //chart.legend.useDefaultMarker = true;

  // Add range selector
  var selector = new am4plugins_rangeSelector.DateAxisRangeSelector();
  selector.container = document.getElementById("controls");
  selector.axis = dateAxis;
  selector.inputDateFormat = "dd-MM-yyyy";

  dateAxis.showOnInit = true;
    chart.events.on("ready", function() {
      var max = dateAxis.max;
      var date1 = new Date(max);
      var date2 = new Date(max);
      am4core.time.add(date1, "year", -1);
      dateAxis.zoomToDates(date1, date2, false, true);
  });
}; // end am4core.ready()




