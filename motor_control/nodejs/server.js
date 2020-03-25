//ffmpeg -s 320x240 -f video4linux2 -i /dev/video0 -f mpeg1video -b 800k -r 30 http://127.0.0.1:8081/chris/640/480/
//ffmpeg -i /dev/video0 -f mpegts -codec:v mpeg1video -s 640x480 -b:v 800k -r 30 http://127.0.0.1:8082/chris/640/480/
//ffmpeg -i in.mp4      -f mpegts -codec:v mpeg1video -s 960x540 -b:v 1500k -r 30 -bf 0 -codec:a mp2 -ar 44100 -ac 1 -b:a 128k out.ts
//ffmpeg -f v4l2 -framerate 20 -video_size 1280x720 -i /dev/video0 -f mpegts -codec:v mpeg1video -s 640x360 -b:v 1000k -bf 0 http://localhost:8081/chris
//raspivid -o - -t 0 -fps 25 -g 50 -rot 180 -n -a 12 -b 6000000 | ffmpeg -f v4l2 -framerate 60 -video_size 1280x720 -i /dev/video0 -f mpegts -codec:v mpeg1video -s 640x360 -b:v 1000k -bf 0 http://localhost:8081/chris


var express = require('express');
var app = express();
var fs = require("fs");
var bodyParser = require('body-parser');
const Gpio = require('pigpio').Gpio;

//Setup the pins for the left motor
const motorLF = new Gpio(23, {mode: Gpio.OUTPUT});
const motorLR = new Gpio(24, {mode: Gpio.OUTPUT});
const motorL_enable = new Gpio(12, {mode: Gpio.OUTPUT});
const motorL_speed_multiplier = 1.7

//Setup the pings for the right motor
const motorRF = new Gpio(17, {mode: Gpio.OUTPUT});
const motorRR = new Gpio(27, {mode: Gpio.OUTPUT});
const motorR_enable = new Gpio(13, {mode: Gpio.OUTPUT});
const motorR_speed_multiplier = 1


//do something when app is closing
process.on('exit', exitHandler.bind(null,{cleanup:true}));

//catches ctrl+c event
process.on('SIGINT', exitHandler.bind(null, {exit:true}));

// catches "kill pid" (for example: nodemon restart)
process.on('SIGUSR1', exitHandler.bind(null, {exit:true}));
process.on('SIGUSR2', exitHandler.bind(null, {exit:true}));

//catches uncaught exceptions
process.on('uncaughtException', exitHandler.bind(null, {exit:true}));

function exitHandler(options, exitCode) {
   if (exitCode || exitCode === 0) console.log(exitCode);
   if (options.exit) process.exit();
}


function set_speed(left_speed,right_speed){
    motorL_enable.pwmWrite(left_speed)
    motorR_enable.pwmWrite(right_speed)
}

function forward(left_speed,right_speed){
    left_speed = left_speed || 80
    right_speed = right_speed || 100
    set_speed(left_speed,right_speed);
    motorLR.digitalWrite(0);
    motorLF.digitalWrite(1);

    motorRR.digitalWrite(0);
    motorRF.digitalWrite(1);
}

function reverse(left_speed,right_speed){
    left_speed = left_speed || 100
    right_speed = right_speed || 80
    set_speed(left_speed,right_speed);
    motorLF.digitalWrite(0);
    motorLR.digitalWrite(1);
    
    motorRF.digitalWrite(0);
    motorRR.digitalWrite(1); 
}

function left(left_speed,right_speed){
    left_speed = left_speed || 80
    right_speed = right_speed || 80
    set_speed(left_speed,right_speed);
    motorLF.digitalWrite(0);
    motorLR.digitalWrite(1);
    
    
    motorRR.digitalWrite(0); 
    motorRF.digitalWrite(1);
}

function right(left_speed,right_speed){
    left_speed = left_speed || 80
    right_speed = right_speed || 80
    set_speed(left_speed,right_speed);
    motorLR.digitalWrite(0);
    motorLF.digitalWrite(1);
    
    motorRF.digitalWrite(0);
    motorRR.digitalWrite(1); 
}

function stop(){
    motorLR.digitalWrite(0);
    motorLF.digitalWrite(0);
    motorRR.digitalWrite(0);
    motorRF.digitalWrite(0);
}



app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true }));
app.use('/static', express.static('public'))

app.get('/status', function (req, res) {
   res.status(200).send("Running")
})


app.delete('/commands', function (req, res) {
   res.status(200).send("Metric counts cleared")
})


app.post('/commands', function (req, res) {
//    req_type = req.body.data[0].type
   console.log(req.body)

   body = JSON.stringify(req.body)
   res.status(200).send(body)

   switch (req.body.command) {
        case 'forward':
            console.log("Forward")
            forward(req.body.lspeed,req.body.rspeed)
            break;
        case "reverse":
            console.log("Reverse")
            reverse(req.body.lspeed,req.body.rspeed)
            break;
        case "left":
            console.log("left")
            left(req.body.lspeed,req.body.rspeed)
            break;
        case "right":
            console.log("right")
            right(req.body.lspeed,req.body.rspeed)
            break;
        case "stop":
            console.log("stop")
            stop()
            break;
   }
   // console.debug({counts})
})








var server = app.listen(5000, '0.0.0.0', function () {
// var server = app.listen(30081, '0.0.0.0', function () {
   var host = server.address().address
   var port = server.address().port
   console.log("Test API listening at http://%s:%s", host, port)
})