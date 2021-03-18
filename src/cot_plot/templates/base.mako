<!DOCTYPE html>
<html lang="en">

<head>
    <%namespace name="ver" file="version.mako"/>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">

    <title>CoT Plot</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-black.css">
    <link rel="preload" href="https://fonts.googleapis.com/css?family=Roboto&display=swap">
    <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

    <link rel="icon" type="image/png" href="/cot_plot/cot_plot/static/images/favicon.png" alt="CotPlot">

    <link href="/cot_plot/cot_plot/static/css/global.css?ver=${ver.app_version()}" rel="stylesheet" type="text/css">

    <script
        src="https://code.jquery.com/jquery-3.6.0.min.js"
        integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4="
        crossorigin="anonymous">
    </script>
    <%block name="header"/>
</head>

<body class="w3-theme-l1">
    ${next.body()}
    <%block name="footer"/>
</body>
</html>


