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
<nav class="w3-sidebar w3-bar-block w3-collapse w3-large w3-theme-l1 w3-animate-left" id="mySidebar">
  <a href="javascript:void(0)" onclick="w3_close()" class="w3-right w3-xlarge w3-padding-large w3-hover-black w3-hide-large" title="Close Menu">
    <i class="fa fa-remove"></i>
  </a>
  <div class="sidebar-title"><b>Symbol</b></div>
  
  % for c in commodities:
  <a id="${c['symbol']}" class="sidebar-item w3-button w3-hover-black tooltip" 
    data-name="${c['name']}"
    onclick="commodity_selection(this)">
    ${c['symbol']}
    <span class="tooltiptext">${c['name']}</span>
  </a>
  % endfor
</nav>

<!-- Overlay effect when opening sidebar on small screens -->
<div class="w3-overlay w3-hide-large" onclick="w3_close()" style="cursor:pointer" title="close side menu" id="myOverlay"></div>

<!-- Main content: shift it to the right by 250 pixels when the sidebar is visible -->
<div class="w3-main" >
  <div class="w3-row w3-padding-32">
    <h2 id="page-item-title" class="pink-text">Select a Commodity</h2>
    <div id="controls" class="chart-controls"></div>
    <div id="chartdiv" class="main-chart"></div>
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
      });

      function commodity_selection(ctrl){
        var url = "${request.current_route_url()}/" + ctrl.id;
        
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                console.log('data success', data);
                $('#page-item-title').text(data['future_name']);
                plot_chart(data['data'])
            }
        });
      };
  </script>
</%block>