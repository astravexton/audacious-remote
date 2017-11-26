#!/usr/bin/python2
import web, commands, re

urls = (
    "/",            "index",
    "/pause",       "pause",
    "/stop",        "stop",
    "/np",          "np",
    "/playlist",    "playlist",
    "/playID=(.*)",  "playSong",
    "/forward", "forward",
    "/backward", "backward",
)

class playSong:
    def GET(self,songID):
        web.header("Content-type","text/html")
        songID = re.sub("[^0-9]","",songID)
        commands.getoutput("audtool playlist-jump {}; audtool playback-play".format(songID))
        return "OK"

class np:
    def GET(self):
        web.header("Content-type","text/html")
        if commands.getoutput("audtool current-song"):
            output = """{} <span class="label label-primary">{}/{}</span>""".format(commands.getoutput("audtool current-song"),commands.getoutput("audtool current-song-output-length"),commands.getoutput("audtool current-song-length"))
        else:
            output = "Nothing Playing"
        if commands.getoutput("audtool playback-status") == "paused":
            output += """ <span class="label label-info">paused</span>"""
        return output

class forward:
    def GET(self):
        web.header("Content-type","text/html")
        return commands.getoutput("audtool playlist-advance")

class backward:
    def GET(self):
        web.header("Content-type","text/html")
        return commands.getoutput("audtool playlist-reverse")

class playlist:
    def GET(self):
        web.header("Content-type","text/html")
        output = """<ul class="list-group">\n"""
        playlist = commands.getoutput("audtool playlist-display").split("\n")[1:-1]
        cursong = commands.getoutput("audtool current-song")
        n=0
        for item in playlist:
            n=n+1
            if cursong in item:
                output+="""\t<li class="list-group-item active">{}</li>\n""".format(item)
            else:
                output+="""\t<li class="list-group-item" onclick="playSong({})">{}</li>\n""".format(str(n),item)
        output+="</ul>\n"
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
    #np {
        text-align: center;
    }
    #np .label {
        margin-left: 5px;
    }
    #footer {
        text-align: center;
    }
    .list-group-item:hover {
        cursor: pointer;
        background-color: rgba(0,0,0,.1);
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
            <button class="btn btn-default btn-success control" id="pause"><i class="fa fa-pause" id="playpause"></i></button>
            <button class="btn btn-default btn-danger control" id="stop"><i class="fa fa-stop"></i></button>
            <button class="btn btn-default btn-warning control" id="forward"><i class="fa fa-forward"></i></button>
        </div>
        </div>
    </div>
    <div class="panel-body" id="playlist"></div>
    <div id="footer" class="clearfix">
        Created by Nathan &copy; 2014<br/>
        View me on <a href="https://github.com/nathan0/audacious-remote">GitHub</a>
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
$("#forward").click(function() {
    $.get("forward");
});
$("#backward").click(function() {
    $.get("backward");
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
        if (html.indexOf("paused") > -1) {
           $("#playpause").removeClass("fa-pause");
           $("#playpause").addClass("fa-play");
        }
        else {
            $("#playpause").removeClass("fa-play");
           $("#playpause").addClass("fa-pause");
        }
    });
    $.ajax({
        url: "/playlist"
    }).done(function(html) {
        $("#playlist").html(html);
    });
}, 1000);
$(".container").fadeIn(1500);
function playSong(songID) {
    $.get("playID="+songID)
}
</script>

<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>

</body>
</html>"""

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
