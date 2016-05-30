<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/css/base.css">
    <script src="/js/jquery-2.2.4.min.js"></script>
    <title> WGPIO v0.2 by Mauro Sauco</title>

</head>
<body>
<H2> WGPIO  Ver. 0.2 </H2>
<table>
    <tbody>
    %for pin in pins[::2]:
        <%
            if pin.channel == 0: ed = ''
            else: ed = 'contenteditable'
        %>
        <tr>
            <td class=name_container> 
                <div class="name">${pin.name}</div>
                <div pid="${pin.pid}" id="label-${pin.pid}" class="label" ${ed}>Click</div>
            </td>
            <td>
                %if pin.channel > 0:
                <div pid="${pin.pid}" id="term-${pin.pid}" class="term unk"></div>
                %endif
            </td>
            <td><div pid="${pin.pid}" id="device-${pin.pid}" class="off"></div></td>
            <td class="pin_container"> 
                <div id="pin-${pin.pid}" class="pin grey">${pin.pid}</div>

            ## +1 to pin
            <% 
                pin = pins[pin.pid]
                if pin.channel == 0: ed = ''
                else: ed = 'contenteditable'
            %>
            
                <div id="pin-${pin.pid}" class="pin grey">${pin.pid}</div>
            </td>
            <td><div pid="${pin.pid}" id="device-${pin.pid}" class="off"></div></td>
            <td>
                %if pin.channel > 0:
                <div pid="${pin.pid}" id="term-${pin.pid}" class="term unk"></div>
                %endif
            </td>
            <td class="name_container"> 
                <div class="name">${pin.name}</div>
                <div pid="${pin.pid}" id="label-${pin.pid}" class="label" ${ed}>Click</div>
            </td> 
        </tr>
    %endfor
    </tbody>
</table>
<script>
 window.pins = null;
    (function poll(){
        $.ajax({ url: "/out", success: function(data){
            window.pins = data;
            $.each( data, function(index, pin ) {
                var pid = pin.pid;
                var label = pin.label;
                var mode = pin.mode;
                var status = pin.status;
                var term = pin.term
                var elabel = $("#label-" + pid);
                var eterm = $("#term-" + pid);
                var edevice = $("#device-" + pid);
                var epin = $("#pin-" + pid);

                if (mode ==-1) dclass = "";
                if (mode == 1) dclass = "push";
                if (mode == 0) dclass = "led";
                if (term ==-1) tclass = 'unk';
                if (term == 1) tclass = 'plus';
                if (term == 0) tclass = 'gnd';
                if (status ==-1) pclass = 'grey';
                if (status == 1) pclass = 'red';
                if (status == 0) pclass = 'green';

                if (!eterm.hasClass(tclass)){
                    eterm.removeClass();
                    eterm.addClass('term ' + tclass);
                };

                if (!epin.hasClass(pclass)){
                    epin.removeClass();
                    epin.addClass("pin "+ pclass);
                }

                if (label != '' && label != elabel.html()){
                    elabel.html(label);
                };
                if(!edevice.hasClass(dclass)){
                    edevice.removeClass("push","led");
                    edevice.addClass(dclass);
                };

                if (mode == 1){
                    if (status != term && term > -1 && status > -1){
                        edevice.removeClass("off");
                        edevice.addClass("on");
                    }else{
                        edevice.removeClass("on");
                        edevice.addClass("off");
                    }
                };

            });
    },  dataType: "json", complete: poll, timeout: 30000 });
    })();
    
    $(document).on('mousedown', '.push', function(){ 
        obj = $(this);
        id = obj.attr("pid");
        epin = $('#pin-' + id); 
        term = window.pins[id -1].term;
        $.ajax({ url: "/in/"+ id +":setstatus:" + term});
        obj.addClass("press");
        epin.removeClass();
        if (term == 0) epin.addClass("pin green");
        if (term == 1) epin.addClass("pin red");
        if (term ==-1) epin.addClass("pin grey");
    });
    $(document).on('mouseup', '.push', function(){
        obj = $(this);
        id = obj.attr("pid");
        epin = $('#pin-' + id);
        term = window.pins[id - 1].term;
        if (term > -1) term = 1 - term;
        $.ajax({url: "/in/"+ id +":setstatus:" + term});
        obj.removeClass("press");
        epin.removeClass();
        if (term == 0) epin.addClass("pin red");
        if (term == 1) epin.addClass("pin green");
        if (term == -1) epin.addClass("pin grey");
    });
    $(document).on('mousedown', '.term', function(){
        obj = $(this);
        id = obj.attr("pid");
        if ( obj.hasClass('unk') ){
            obj.removeClass('unk');
            obj.addClass('plus');
            $.ajax({ url: "/in/"+ id +":setterm:1"});
            return;
       }
        if ( obj.hasClass('plus') ){
            obj.removeClass('plus');
            obj.addClass('gnd');
            $.ajax({ url: "/in/"+ id +":setterm:0"});
            return;
       }
        if ( obj.hasClass('gnd') ){
            obj.removeClass('gnd');
            obj.addClass('unk');
            $.ajax({ url: "/in/"+ id +":setterm:-1"});
            return;
       }
    });
    $(document).on('focusout','.label',function(){
        label = $(this).html();
        if (label == '') label = 'Click'
        id = $(this).attr('pid')
        $.ajax({url: "/in/"+ id +":setlabel:" + label});

    });
    $(document).on('focusin','.label',function(){
        label = $(this).html();
        console.log(label);
        if (label == "Click") $(this).html("");
    });

</script>
</body>
</html>