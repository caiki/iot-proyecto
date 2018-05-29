            $(window).load(function() {
                var item = $(".item");

                // agrego la clase blur a todos los 'item' que NO sea al que le se le esta aplicando el evento 'hover'
                item.hover(function() {
                    item.not($(this)).addClass('blur');
                    // al perder el foco, retiro la clase a todos los 'item'
                }, function() {
                    item.removeClass('blur');
                });
                item.click(function() {
                    item.not($(this)).addClass('blur');
                    // al perder el foco, retiro la clase a todos los 'item'
                }, function() {
                    item.removeClass('blur');
                });
            });
