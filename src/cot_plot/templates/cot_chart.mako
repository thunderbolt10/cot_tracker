<%inherit file="base_menus.mako"/>
<%namespace name="ver" file="version.mako"/>

<%block name="header">
  <style>
      html,body,h1,h2,h3,h4,h5,h6 {font-family: "Roboto", sans-serif;}
      .w3-sidebar {
          z-index: 3;
          width: 250px;
          top: 45px;
          bottom: 0;
          height: inherit;
      }
  </style>

  

  <script src="https://cdn.amcharts.com/lib/4/core.js"></script>
  <script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
  <script src="https://cdn.amcharts.com/lib/4/themes/material.js"></script>
</%block>

<!-- Sidebar -->
<nav class="w3-sidebar w3-bar-block w3-collapse w3-large  w3-animate-left my-theme" id="mySidebar">
  <a href="javascript:void(0)" onclick="w3_close()" class="w3-right w3-xlarge w3-padding-large w3-hover-black w3-hide-large" title="Close Menu">
    <i class="fa fa-remove"></i>
  </a>
  <div class="sidebar-title">
    <div class="w3-row ">
      <div class="w3-col" style="width:30%"><b>Symbol</b></div>
      <div class="w3-col" style="width:23%; text-align: right"><b>Price</b></div>
      <div class="w3-col" style="width:23%; text-align: right"><b>Chg</b></div>
      <div class="w3-col" style="width:23%; text-align: right"><b>% Chg</b></div>
    </div>
  </div>
  
  % for c in commodities:
  <a id="${c['symbol']}" class="sidebar-item w3-button w3-hover-black " 
    data-name="${c['name']}"
    onclick="commodity_selection(this)">
    <div class="w3-row ">
      <div class="w3-col" style="width:30%">${c['symbol']}</div>  
      <div id="${c['symbol']}-price" class="w3-col com-value" style="width:23%"></div>
      <div id="${c['symbol']}-change" class="w3-col com-value" style="width:23%"></div>
      <div id="${c['symbol']}-pchange" class="w3-col com-value" style="width:23%"></div>
    </div>
    
  </a>
  % endfor
</nav>

<!-- Overlay effect when opening sidebar on small screens -->
<div class="w3-overlay w3-hide-large" onclick="w3_close()" style="cursor:pointer" title="close side menu" id="myOverlay"></div>

<!-- Main content: shift it to the right by 250 pixels when the sidebar is visible -->
<div class="w3-main" >
  <div class="w3-row w3-padding-32">
    <h5 id="page-item-title" class="pink-text">Select a Commodity</h5>
    <div id="chartdiv" class="main-chart"></div>
    <div id="controls" class="chart-controls"></div>
  </div>
  
<!-- END MAIN -->
</div>


<%block name="footer">
  <!-- Resources -->
  <script src="https://cdn.amcharts.com/lib/4/core.js"></script>
  <script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
  <script src="https://cdn.amcharts.com/lib/4/plugins/rangeSelector.js"></script>
  <script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>
  <script src="https://cdn.amcharts.com/lib/4/themes/amchartsdark.js"></script>

  <script src="/cot_plot/cot_plot/static/js/commodities.js"></script>

  <script>
      // Get the Sidebar
      var mySidebar = document.getElementById("mySidebar");

      // Get the DIV with overlay effect
      var overlayBg = document.getElementById("myOverlay");

      // Toggle between showing and hiding the sidebar, and add overlay effect
      function w3_open() {
        if (mySidebar.style.display === 'block') {
            mySidebar.style.display = 'none';
            overlayBg.style.display = "none";
        } else {
            mySidebar.style.display = 'block';
            overlayBg.style.display = "block";
        }
      }

      // Close the sidebar with the close button
      function w3_close() {
        mySidebar.style.display = "none";
        overlayBg.style.display = "none";
      }

      $( document ).ready(function() {
        $('#commodity-page-light').addClass('pink-bkg');
        update_prices();
      });

      function commodity_selection(ctrl){
        var url = "${request.current_route_url()}/" + ctrl.id;
        
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                $('#page-item-title').text(data['future_name']);
                plot_chart(data['cot'], data['price'])
            }
        });
      };
    
      var timer = setInterval(update_prices, 60000);

      function update_prices() {
        
        var url = "${request.route_url('cot_prices')}";
        
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
              for (i in data) {
                var item = data[i];

                $('#' + item['symbol'] + '-price').text(item['price']);
                $('#' + item['symbol'] + '-change').text(item['change']);
                $('#' + item['symbol'] + '-pchange').text(item['% change']);

                if (item['change'] >= 0.0) {
                  $('#' + item['symbol'] + '-change').removeClass('negative-value')
                } else {
                  $('#' + item['symbol'] + '-change').addClass('negative-value')
                }

                
                if (item['% change'] >= 0.0) {
                  $('#' + item['symbol'] + '-change').removeClass('negative-value')
                } else {
                  $('#' + item['symbol'] + '-pchange').addClass('negative-value')
                }
              }
           }
        });
      };

      

      
  </script>
</%block>