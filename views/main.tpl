<!DOCTYPE html>
<%! UNDEFINED="" %> 
<html>
<head>
    <link rel="stylesheet" href="/css/base.css">
    <script src="/js/jquery-2.2.4.min.js"></script>

</head>
<body>
<table>
    %for pin in pins[::2]:
        <tr>
            <td class=name_container> 
                <div class="name">${pin.name}</div>
                <div pid="${pin.pid}" id="label-${pin.pid}" class="label">CLick</div>
            </td>
            <td>
                %if pin.channel > 0:
                <div pid="${pin.pid}" id="polarity-${pin.pid}" class="polarity right unk"></div>
                %endif
            </td>
            <td><div pid="${pin.pid}" id="device-${pin.pid}"></div></td>
            <td class="pin_container"> 
                <div id="pin-${pin.pid}" class="pin">${pin.pid}</div>

            ## adding one to pin
            <% pin = pins[pin.pid] %> 
            
                <div id="pin-${pin.pid}" class="pin">${pin.pid}</div>
            </td>
            <td><div pid="${pin.pid}" id="device-${pin.pid}"></div></td>
            <td>
                %if pin.channel > 0:
                <div pid="${pin.pid}" id="polarity-${pin.pid}" class="polarity left unk"></div>
                %endif
            </td>
            <td class="name_container"> 
                <div class="name">${pin.name}</div>
                <div pid="${pin.pid}" id="label-${pin.pid}" class="label">CLick</div>
            </td> 
        </tr>
    %endfor
</table>
<script>
var x;
    (function poll(){
        $.ajax({ url: "/out", success: function(data){
            $.each( data, function(index, pin ) {
                if (pin['label'] != ''){
                    $("#label-" + pin['pid']).html(pin['label']);
                };
                if($("#device-" + pin['pid']).attr('class') != pin['device']){
                    $("#device-" + pin['pid']).removeClass();
                    $("#device-" + pin['pid']).addClass(pin['device']);
                };

                if (pin['device'] == "led" && pin['status'] == "on"){
                    $("#device-" + pin['pid']).addClass("on");
                };
            });
    },  dataType: "json", complete: poll, timeout: 30000 });
    })();
    
    $(document).on('mousedown', '.push', function(){
       console.log(this.id); 

    });
    $(document).on('mouseup', '.push', function(){
       console.log("yop"); 
    });

    $(document).on('mousedown', '.polarity', function(){
        obj = $(this);
        id = obj.attr("pid");

        if ( obj.hasClass('unk') ){
            obj.removeClass('unk');
            obj.addClass('plus');
            $.ajax({ url: "/in/"+ id +":setpolarity:1"});
            return;
       }
        if ( obj.hasClass('plus') ){
            obj.removeClass('plus');
            obj.addClass('gnd');
            $.ajax({ url: "/in/"+ id +":setpolarity:0"});
            return;
       }
        if ( obj.hasClass('gnd') ){
            obj.removeClass('gnd');
            obj.addClass('unk');
            $.ajax({ url: "/in/"+ id +":setpolarity:-1"});
            return;
       }

    });
</script>

</body>
</html>