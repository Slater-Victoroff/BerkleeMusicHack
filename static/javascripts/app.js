
$(document).ready(function() {

    circles = [];

    var res = {'x': 600.0, 'y': 480.0} 
    var w = $(window).width();
    var h = $(window).height();

    var scale_x = w/res['x']
    var scale_y = h/res['y']

    // Make an instance of two and place it on the page.
    var elem = document.getElementById('two');
    var params = { width: w, height: h};
    var two = new Two(params).appendTo(elem);

    var colors = [["#3498db", "#2980b9"], ["#f1c40f", "#f39c12"], ["#2ecc71", "#27ae60"], ["#9b59b6", "#8e44ad"], ["#e67e22", "#d35400"]];
    var circle = function(x, y, r, color_index) {
        var c = two.makeCircle(x*scale_x, y*scale_y, r);
        c.fill = colors[color_index][0];
        c.stroke = colors[color_index][1];
        c.linewidth = 5;
        c.opacity = 1.0;
        c.scale = 1.0
        circles.push(c);
        return c;
    }

    var c = circle(300, 240, 20, 0)
    // Don't forget to tell two to render everything
    // to the screen
    two.update();

    var ws = new WebSocket("ws://localhost:8888/ws");
    ws.onopen = function() {
      console.log("Socket opened.")
      ws.send("Socket opened.");
    };
    ws.onmessage = function (evt) {
      var data = JSON.parse(evt.data);
      var c = circle(data.x, data.y, data.r, data.note);
      two.update()
    };

    var update = function() {
        for (var c in circles) {
            circles[c].opacity *= 0.95;
            circles[c].scale *= 1.02;
            if (circles[c].opacity < 0.05) {
                two.remove(circles[c]);
            }
            two.update()
        }
    }

    setInterval(update, 10);

})
