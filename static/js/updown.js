(function () {

    var request_url = null; /* 保存请求的url*/

    var that = null;    /* 保存请求的当前标签对象*/

    function bindUp(){
        $('.fa-thumbs-o-up').parent().click(function () {
            that = this;
            var nid = $(this).parent().attr('id');
            $.ajax({
                url:request_url,
                type:'GET',
                data:{'nid':nid,'up':1},
                dataType:'JSON',
                success:function (arg) {
                    if(arg.status){
                        UpAdd(that);
                    }
                    else {
                        UpCut(that)
                    }
                }
            });
        });
    }

    function UpAdd(ths) {
        var fontSize = 15;
        var top = 0;
        var right = 0;
        var opacity = 1;

        var tag = document.createElement('span');
        $(tag).text('+1');
        $(tag).css('color', 'green');
        $(tag).css('position', 'absolute');
        $(tag).css('fontSize', fontSize + "px");
        $(tag).css('right', right + "px");
        $(tag).css('top', top + 'px');
        $(tag).css('opacity', opacity);
        $(ths).append(tag);

        var a = $(ths).children().first().next();
        a.text(parseInt(a.text()) + 1);
        $(ths).css('color', 'green');

        var obj = setInterval(function () {
            fontSize = fontSize + 8;
            top = top - 10;
            right = right - 10;
            opacity = opacity - 0.1;

            $(tag).css('fontSize', fontSize + "px");
            $(tag).css('right', right + "px");
            $(tag).css('top', top + 'px');
            $(tag).css('opacity', opacity);
            if (opacity < 0) {
                clearInterval(obj);
                $(tag).remove();
            }
        }, 40);
    }

    function UpCut(ths) {
        var fontSize = 15;
        var top = 0;
        var right = 0;
        var opacity = 1;

        var tag = document.createElement('span');
        $(tag).text('-1');
        $(tag).css('color','gray');
        $(tag).css('position','absolute');
        $(tag).css('fontSize',fontSize + "px");
        $(tag).css('right',right + "px");
        $(tag).css('top',top + 'px');
        $(tag).css('opacity',opacity);
        $(ths).append(tag);

        var a = $(ths).children().first().next();
        a.text(parseInt(a.text())-1);
        $(ths).css('color','gray');

        var obj = setInterval(function () {
            fontSize = fontSize + 8;
            top = top - 10;
            right = right - 10;
            opacity = opacity - 0.1;

            $(tag).css('fontSize',fontSize + "px");
            $(tag).css('right',right + "px");
            $(tag).css('top',top + 'px');
            $(tag).css('opacity',opacity);
            if(opacity < 0){
                clearInterval(obj);
                $(tag).remove();
            }
        }, 40);
    }

    function bindDown(){
        $('.fa-thumbs-o-down').parent().click(function () {
            that = this;
            var nid = $(this).parent().attr('id');
            $.ajax({
                url:request_url,
                type:'GET',
                data:{'nid':nid,'up':0},
                dataType:'JSON',
                success:function (arg) {
                    if(arg.status){
                        DownAdd(that);
                    }
                    else {
                        DownCut(that)
                    }
                }
            });
        });
    }

    function DownAdd(ths) {
        var fontSize = 15;
        var top = 0;
        var right = 0;
        var opacity = 1;

        var tag = document.createElement('span');
        $(tag).text('+1');
        $(tag).css('color', 'red');
        $(tag).css('position', 'absolute');
        $(tag).css('fontSize', fontSize + "px");
        $(tag).css('right', right + "px");
        $(tag).css('top', top + 'px');
        $(tag).css('opacity', opacity);
        $(ths).append(tag);

        var a = $(ths).children().first().next();
        a.text(parseInt(a.text()) + 1);
        $(ths).css('color', 'red');

        var obj = setInterval(function () {
            fontSize = fontSize + 8;
            top = top - 10;
            right = right - 10;
            opacity = opacity - 0.1;

            $(tag).css('fontSize', fontSize + "px");
            $(tag).css('right', right + "px");
            $(tag).css('top', top + 'px');
            $(tag).css('opacity', opacity);
            if (opacity < 0) {
                clearInterval(obj);
                $(tag).remove();
            }
        }, 40);
    }

    function DownCut(ths) {
        var fontSize = 15;
        var top = 0;
        var right = 0;
        var opacity = 1;

        var tag = document.createElement('span');
        $(tag).text('-1');
        $(tag).css('color','gray');
        $(tag).css('position','absolute');
        $(tag).css('fontSize',fontSize + "px");
        $(tag).css('right',right + "px");
        $(tag).css('top',top + 'px');
        $(tag).css('opacity',opacity);
        $(ths).append(tag);

        var a = $(ths).children().first().next();
        a.text(parseInt(a.text())-1);
        $(ths).css('color','gray');

        var obj = setInterval(function () {
            fontSize = fontSize + 8;
            top = top - 10;
            right = right - 10;
            opacity = opacity - 0.1;

            $(tag).css('fontSize',fontSize + "px");
            $(tag).css('right',right + "px");
            $(tag).css('top',top + 'px');
            $(tag).css('opacity',opacity);
            if(opacity < 0){
                clearInterval(obj);
                $(tag).remove();
            }
        }, 40);
    }

    jQuery.extend({
        'UpDown':function (url) {
            request_url=url;
            bindUp();
            bindDown();
        }
    });
})();