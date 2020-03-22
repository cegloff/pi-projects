const Gpio = require('pigpio').Gpio;

//Setup the pins for the left motor
const motorLF = new Gpio(17, {mode: Gpio.OUTPUT});
const motorLR = new Gpio(27, {mode: Gpio.OUTPUT});
const motorL_enable = new Gpio(12, {mode: Gpio.OUTPUT});
const motorL_speed_multiplier = 1.7

//Setup the pings for the right motor
const motorRF = new Gpio(23, {mode: Gpio.OUTPUT});
const motorRR = new Gpio(24, {mode: Gpio.OUTPUT});
const motorR_enable = new Gpio(13, {mode: Gpio.OUTPUT});
const motorR_speed_multiplier = 1

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
        currentDate = Date.now();
    } while (currentDate - date < milliseconds);
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
    set_speed(left_speed,right_speed);
    motorLF.digitalWrite(0);
    motorLR.digitalWrite(1);
    
    
    motorRR.digitalWrite(0); 
    motorRF.digitalWrite(1);
}

function right(left_speed,right_speed){
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




// Test the functions to verify wiring
forward(80,100);
sleep(3000);
reverse(100,80);
sleep(3000);
right(125,125)
sleep(3000)
left(125,125)
sleep(3000)
stop();