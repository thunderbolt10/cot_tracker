<%inherit file="base.mako"/>
<%namespace name="ver" file="version.mako"/>


<!-- Navbar -->
<div class="w3-top">
  <div class="w3-bar w3-theme w3-top w3-left-align w3-large">
    <a class="w3-bar-item w3-button w3-right w3-hide-large w3-hover-white w3-large w3-theme-l1" href="javascript:void(0)" onclick="w3_open()">
        <i class="fa fa-bars"></i>
    </a>
    
    <a href="#" class="w3-button app-title">
        <img src="/cot_plot/cot_plot/static/images/favicon.png" style="height: 28px; width: 28px;"/>
        <span class="w3-margin-left w3-margin-right">CoT Tracker<span>
    </a>
    <ol class="w3-ul w3-bar-item w3-hide-small" style="padding: 0px;">
        <li style="padding: 0px;">
            <a href="/cot_plot/cot/chart" class="w3-button w3-hover-white">Commodities</a>
        </li>
        <li id="commodity-page-light" class="page-btn-light"></li>
    </ol>
    <ol class="w3-ul w3-bar-item w3-hide-small" style="padding: 0px;">
        <li style="padding: 0px;">
            <a href="#" class="w3-button w3-hover-white">Currencies/Bonds</a>
        </li>
        <li id="currency-page-light" class="page-btn-light"></li>
    </ol>
    <ol class="w3-ul w3-bar-item w3-hide-small" style="padding: 0px;">
        <li style="padding: 0px;">
            <a href="#" class="w3-button w3-hover-white">Stocks</a>
        </li>
        <li id="stock-page-light" class="page-btn-light"></li>
    </ol>

  </div>
</div>

${next.body()}
