import web, commands

urls = (
    "/",      "index",
    "/pause", "pause",
    "/stop",  "stop",
    "/np",    "np",
    "/playlist",    "playlist",
)

pl = commands.getoutput("audtool current-song")
f = open("/tmp/audaciouspl","w")
f.write(pl)
f.close()

class np:
    def GET(self):
        web.header("Content-type","text/html")
        if commands.getoutput("audtool current-song"):
            output = commands.getoutput("audtool current-song")+" <span class=\"label label-primary\">"+commands.getoutput("audtool current-song-output-length")+"/"+commands.getoutput("audtool current-song-length")+"</span>"
        else:
            output = "Nothing Playing"
        if commands.getoutput("audtool playback-status") == "paused":
            output += """ <span class="label label-info">paused</span>"""
        return output

class playlist:
    def GET(self):
        web.header("Content-type","text/html")
        output = """<ul class="list-group">"""
        playlist = commands.getoutput("audtool playlist-display").split("\n")[1:-1]
        cursong = commands.getoutput("audtool current-song")
        for item in playlist:
            if cursong in item:
                output+="""<li class="list-group-item active">"""+item+"</li>"
            else:
                output+="""<li class="list-group-item">"""+item+"</li>"
        output+="</ul>"
        return output.replace(" - "," <strong>-</strong> ")

class pause:
    def GET(self):
        web.header("Content-type","text/html")
        return commands.getoutput("audtool playback-playpause")

class stop:
    def GET(self):
        web.header("Content-type","text/html")
        return commands.getoutput("audtool playback-stop")

class index:
    def GET(self):
        return """<!DOCTYPE html>
<html>
<head>
    <title>Audacious Remote Player</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <meta content='yes' name='apple-mobile-web-app-capable'>
    <style>
    *{margin:0;padding:0;}
    body { padding-bottom: 30px; }
    .control {
        //width: 30px;
        //height: 30px;
    }
    .controls {
        //position: absolute;
        //top: 0;
        //left: 0;
    }
    #np {
        text-align: center;
    }
    #np .label {
        margin-left: 5px;
    }
    #footer {
        text-align: center;
    }
    </style>
    <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css" rel="stylesheet" />
    <link href="//maxcdn.bootstrapcdn.com/bootswatch/3.2.0/lumen/bootstrap.min.css" rel="stylesheet">
    <script src="//code.jquery.com/jquery-2.1.1.min.js"></script>
</head>
<body>

<div class="navbar navbar-default" role="navigation">
    <div class="container-fluid">
        <div class="navbar-header">
            <a class="navbar-brand" href="/">Audacious Remote Player</a>
        </div>
    </div>
</div>
<div class="container" style="margin-top:10px;display:none;">
    <div class="panel panel-default">
        <div class="panel-heading" id="np"></div>
        <div style="text-align:center;">
        <div class="controls panel-body">
            <button class="btn btn-default btn-warning control" id="backward"><i class="fa fa-backward"></i></button>
            <button class="btn btn-default btn-success control" id="pause"><i class="fa fa-pause"></i></button>
            <button class="btn btn-default btn-danger control" id="stop"><i class="fa fa-stop"></i></button>
            <button class="btn btn-default btn-warning control" id="forward"><i class="fa fa-forward"></i></button>
        </div>
        </div>
    </div>
    <div class="panel-body" id="playlist"></div>
    <div id="footer" class="clearfix">
        Created by Nathan &copy; 2014<br/>
        View me on <a href="">GitHub</a>
    </div>
</div>

<script>
$.ajax({
    url: "/np"
}).done(function(html) {
    $("#np").html(html);
});
$.ajax({
    url: "/playlist"
}).done(function(html) {
    $("#playlist").html(html);
});
$("#pause").click(function() {
    $.get("pause");
});
$("#stop").click(function() {
    $.get("stop");
});
setInterval(function(){
    $.ajax({
        url: "/np"
    }).done(function(html) {
        $("#np").html(html);
    });
    $.ajax({
        url: "/playlist"
    }).done(function(html) {
        $("#playlist").html(html);
    });
}, 1000);
$(".container").fadeIn(1500);
</script>

<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>

</body>
</html>"""

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

