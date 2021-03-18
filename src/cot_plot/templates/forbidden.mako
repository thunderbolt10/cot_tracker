<%inherit file="base_menus.mako"/>
<%namespace name="ver" file="version.mako"/>

<%def name="get_value(record, field_name, default)" filter="trim">
    % if record is not None and field_name in record:
        %if isinstance(record[field_name], list):
            ${str(record[field_name]).strip('[]')}
        %else:
            ${record[field_name]}
        %endif
    % else:
        ${default}
    % endif

</%def>
<!-- Page Content -->
<div id="page-wrapper">
    <div class="container-fluid">
        <div class="row" style="">
            <div class="col-lg-12">

                <h1 class="page-header" style="margin-bottom: 0px;">Access Restricted</h1>

                <p>You are not allowed' to view this page</p>
                <p>403 Forbidden</p>

            </div>
            <!-- /.col-lg-12 -->
        </div>
        <!-- /.row -->
    </div>
    <!-- /.container-fluid -->
</div>
<!-- /#page-wrapper -->


<%block name="footer">

</%block>

