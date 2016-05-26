<!DOCTYPE html>
<%! UNDEFINED="" %> 
<html>
<head>
    <link rel="stylesheet" href="/css/base.css">
    <script src="/js/jquery-2.2.4.min.js"></script>

</head>
<body>

<div class="container">
    %for pin in pins[::2]:
        <div class="liner">
            <div class="name"> 
                <div class="sname">${pin.name}</div>
                <div id="label-${pin.pid}" class="label">CLick</div>
            </div>
            <div class="none">&nbsp;</div>
            <div id="device-${pin.pid}" class="none">&nbsp;</div>
            <div class="none">&nbsp;</div>
            <div class="pin">${pin.pid}</div>
        </div>
    %endfor
</div>
<div class="container">
    %for pin in pins[1::2]:
        <div class="liner">
            <div class="pin">${pin.pid}</div>
            <div class="none">&nbsp;</div>
            <div id="device-${pin.pid}" class="none">&nbsp;</div>
            <div class="none">&nbsp;</div>
            <div class="none">&nbsp;</div>
            <div class="none">&nbsp;</div>
            <div class="none">&nbsp;</div>
            <div class="name"> 
                <div class="sname">${pin.name}</div>
                <div id="label-${pin.pid}" class="label">CLick</div>
            </div>
        </div>
    %endfor
</div>
    <script>

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
    </script>

</body>
</html>