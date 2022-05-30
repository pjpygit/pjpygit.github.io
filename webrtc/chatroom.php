<?php

$a=$_REQUEST['a'];
session_start();
  include_once "../database/db_conection.php";
  if(!isset($_SESSION['email'])){
    header("location: ../index.php");
  }
?>



<!DOCTYPE html>
<html lang="en">
<head>
    <!-- icon -->
    <link rel="shortcut icon" href="favicon.ico">

    <!-- socketio -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.1/socket.io.js" integrity="sha512-9mpsATI0KClwt+xVZfbcf2lJ8IFBAwsubJ6mI3rtULwyM3fBmQFzj0It4tGqxLOGQwGfJdk/G+fANnxfq9/cew==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
	
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <!-- jQuery library -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <!-- Popper JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <!-- Latest compiled JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

    <!-- google Material icons -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
   
    <!-- custom css -->
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="chatroom.css">
    

    <script type="text/javascript"> 
        var myRoomID = "{{room_id}}"; 
        var myName = "{{display_name}}"; 
        var audioMuted = "{{mute_audio}}"=="1";
        var videoMuted = "{{mute_video}}"=="1";
        console.log(">> {{mute_audio}}, {{mute_video}}", audioMuted, videoMuted);
    </script>
    <script src="chatroom_ui.js"></script>
    <script src="chatroom_networking.js"></script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Chat [room_id]</title>
</head>
<body>
    
     
<div id="room_link"></div>
       
        
    <div class="container-fluid px-0 mx-0">
        <div id="video_grid" class="video-grid"></div>

        <div id="control_box" class="row control-box shadow">
            <div class="col-7 col-md-8 col-lg-9 d-flex justify-content-around align-items-center button-box">
                
                <button id="bttn_mute" class="btn btn-lg btn-outline-secondary rounded-circle">
                    <span id="mute_icon" class="material-icons pt-2">
                        mic
                    </span>
                </button>
                <button id="bttn_vid_mute"class="btn btn-lg btn-outline-secondary rounded-circle">
                    <span id="vid_mute_icon" class="material-icons pt-2">
                        videocam
                    </span>
                </button>
                <button id="call_end" class="btn btn-lg btn-danger rounded-circle">
                    <span class="material-icons pt-2">
                        call_end
                    </span>
                </button>
            </div>
            <div id="div_local_vid" class="col-5 col-md-4 col-lg-3 video-item ml-auto">
                <div class="vid-wrapper">
                    <video id="local_vid" autoplay muted></video>
                </div>
            </div>
        </div>
    </div>    
</body>
</html>