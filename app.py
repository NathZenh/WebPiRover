# Import packages for Camera
import io
import picamera
import logging
import socketserver
from threading import Condition
# Import packages for Webserver
from http import server
# Import packages for GPIO
import RPi.GPIO as GPIO

#GPIO Pins zuweisen (in bcm numbering)
pin4 = 26 #     PIN 37 -> B-A2 [Green]
pin3 = 20 #     PIN 38 -> B-A1 [Blue]
# GPIO 5V power PIN 4 -> VCC [Orange]
# GPIO Ground   PIN 14 -> GND [Yellow]
pin1 = 16 #     PIN 36 -> A-A2 [Brown]
pin2 = 19 #     PIN 35 -> A-A1 [Red]

# GPIO Pins initialisieren
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)

# Give PWM output to pins
pwmLF=GPIO.PWM(pin1, 50)  # Frequenz [Hz]
pwmLF.start(0)		# Initialer Duty Cycle
pwmRF=GPIO.PWM(pin3, 50)  # Frequenz [Hz]
pwmRF.start(0)		# Initialer Duty Cycle

pwmLB=GPIO.PWM(pin2, 50)  # Frequenz [Hz]
pwmLB.start(0)		# Initialer Duty Cycle
pwmRB=GPIO.PWM(pin4, 50)  # Frequenz [Hz]
pwmRB.start(0)		# Initialer Duty Cycle

# Define the HTML to be sent to the browser
PAGE="""\
<html>
    <head>
        <title>NathZenh - Raspi Mini Car</title>
        <link rel="shortcut icon" href="https://nathzenh.ch/assets/images/logo.ico" type="image/x-icon">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
        <script>
            $(document).ready(function(){
                // make submit button send ajax request
                // so that the page doesn't refresh
                $('input[type="submit"]').click(function(e) {
                    e.preventDefault();

                    $.ajax({
                        type: 'POST',
                        url: '/',
                        data: { submit: this.value },
                        success: function(response) {
                        }
                    });
                });
                // make WASD keys press triggers the submit buttons
                $("body").keydown(function(event){
                    if(event.which == 87) {
                        $('#w_d').trigger('click');
                        $('#w').css('box-shadow', '0 0 5px 5px #717c85');
                    }
                    if(event.which == 65) {
                        $('#a_d').trigger('click');
                        $('#a').css('box-shadow', '0 0 5px 5px #717c85');
                    }
                    if(event.which == 83) {
                        $('#s_d').trigger('click');
                        $('#s').css('box-shadow', '0 0 5px 5px #717c85');
                    }
                    if(event.which == 68) {
                        $('#d_d').trigger('click');
                        $('#d').css('box-shadow', '0 0 5px 5px #717c85');
                    }
                    // NOTSTOP!
                    if(event.which == 88) {
                        $('#x').trigger('click');
                        $('body').css('color', 'red');
                    }
                });
                // make WASD keys release triggers the submit buttons
                $("body").keyup(function(event){
                    if(event.which == 87) {
                        $('#w_u').trigger('click');
                        $('#w').css('box-shadow', 'none');
                    }
                    if(event.which == 65) {
                        $('#a_u').trigger('click');
                        $('#a').css('box-shadow', 'none');
                    }
                    if(event.which == 83) {
                        $('#s_u').trigger('click');
                        $('#s').css('box-shadow', 'none');
                    }
                    if(event.which == 68) {
                        $('#d_u').trigger('click');
                        $('#d').css('box-shadow', 'none');
                    }
                });
            });
        </script>
        <style>
            body {
                line-height: 0.3;
                font-family: 'Share Tech', sans-serif;
                font-size: 68px;
                color: white;
                margin: 0;
                width: 100vw;
                height: 95vh;
                text-shadow: 8px 8px 10px #0000008c;
                background-color: #343a40;
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='49' viewBox='0 0 28 49'%3E%3Cg fill-rule='evenodd'%3E%3Cg id='hexagons' fill='%239C92AC' fill-opacity='0.25' fill-rule='nonzero'%3E%3Cpath d='M13.99 9.25l13 7.5v15l-13 7.5L1 31.75v-15l12.99-7.5zM3 17.9v12.7l10.99 6.34 11-6.35V17.9l-11-6.34L3 17.9zM0 15l12.98-7.5V0h-2v6.35L0 12.69v2.3zm0 18.5L12.98 41v8h-2v-6.85L0 35.81v-2.3zM15 0v7.5L27.99 15H28v-2.31h-.01L17 6.35V0h-2zm0 49v-8l12.99-7.5H28v2.31h-.01L17 42.15V49h-2z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E"), linear-gradient(to right top, #343a40, #2b2c31, #211f22, #151314, #000000);
            }
            h1 {
                margin-top: 5vh;
            }
            .key {
                line-height: normal;
                background-color: #343a40;
                /*border: #000000 2px solid;*/
                width: 6vw;
                margin: 4px;
            }
            .onerow {
                float: left;
            }
            #onerow {
                padding: 0 40vw;
            }
        </style>
    </head>
    <body>
        <center>
            <h1>NathZenh</h1>
            <h3>Raspi Mini Car</h3>
        </center>
        <!-- Video Stream Output -->
        <center>
            <img src="stream.mjpg" width="640" height="480">
        </center>
        <!-- Hidden submit Buttons -->
        <form action="/" method="POST">
            <input type="submit" name="submit" value="w_d" id="w_d" hidden>
            <input type="submit" name="submit" value="a_d" id="a_d" hidden>
            <input type="submit" name="submit" value="s_d" id="s_d" hidden>
            <input type="submit" name="submit" value="d_d" id="d_d" hidden>
            <input type="submit" name="submit" value="w_u" id="w_u" hidden>
            <input type="submit" name="submit" value="a_u" id="a_u" hidden>
            <input type="submit" name="submit" value="s_u" id="s_u" hidden>
            <input type="submit" name="submit" value="d_u" id="d_u" hidden>
            <input type="submit" name="submit" value="x" id="x" hidden>
        </form>
        <center>
            <div id="w" class="key">W</div>
            <div id="onerow">
                <div id="a" class="key onerow">A</div>
                <div id="s" class="key onerow">S</div>
                <div id="d" class="key onerow">D</div>
            </div>
        </center>
    </body>
</html>
"""

# Define the MIME type for the video stream
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

# Define the variables for the WASD keys
w = False
a = False
s = False
d = False

# Define the HTTP server
class StreamingHandler(server.BaseHTTPRequestHandler):
    # controll gpio pins form post data
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]

        global w
        global a
        global s
        global d

        if post_data == 'w_d':
            w = True
        if post_data == 'a_d':
            a = True
        if post_data == 's_d':
            s = True
        if post_data == 'd_d':
            d = True
        if post_data == 'w_u':
            w = False
        if post_data == 'a_u':
            a = False
        if post_data == 's_u':
            s = False
        if post_data == 'd_u':
            d = False
        # NOTSTOP!
        if post_data == 'x':
            print("NOTSTOP!")
            camera.stop_recording()
            pwmLF.stop()
            pwmLB.stop()
            pwmRF.stop()
            pwmRB.stop()
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.LOW)
            GPIO.output(pin3, GPIO.LOW)
            GPIO.output(pin4, GPIO.LOW)
        # Forward
        if w == True and s == False and a == d:
            pwmLF.ChangeDutyCycle(100)
            pwmRF.ChangeDutyCycle(100)
            pwmLB.ChangeDutyCycle(0)
            pwmRB.ChangeDutyCycle(0)
        # Forward Left
        if w == True and a == True and s == False and d == False:
            pwmLF.ChangeDutyCycle(50)
            pwmRF.ChangeDutyCycle(100)
            pwmLB.ChangeDutyCycle(0)
            pwmRB.ChangeDutyCycle(0)
        # Forward Right
        if w == True and a == False and s == False and d == True:
            pwmLF.ChangeDutyCycle(100)
            pwmRF.ChangeDutyCycle(50)
            pwmLB.ChangeDutyCycle(0)
            pwmRB.ChangeDutyCycle(0)
        # Backward
        if w == False and s == True and a == d:
            pwmLF.ChangeDutyCycle(0)
            pwmRF.ChangeDutyCycle(0)
            pwmLB.ChangeDutyCycle(100)
            pwmRB.ChangeDutyCycle(100)
        # Backward Left
        if w == False and a == True and s == True and d == False:
            pwmLF.ChangeDutyCycle(0)
            pwmRF.ChangeDutyCycle(0)
            pwmLB.ChangeDutyCycle(50)
            pwmRB.ChangeDutyCycle(100)
        # Backward Right
        if w == False and a == False and s == True and d == True:
            pwmLF.ChangeDutyCycle(0)
            pwmRF.ChangeDutyCycle(0)
            pwmLB.ChangeDutyCycle(100)
            pwmRB.ChangeDutyCycle(50)
        # Left
        if a == True and d == False and w == s:
            pwmLF.ChangeDutyCycle(0)
            pwmRF.ChangeDutyCycle(100)
            pwmLB.ChangeDutyCycle(100)
            pwmRB.ChangeDutyCycle(0)
        # Right
        if a == False and d == True and w == s:
            pwmLF.ChangeDutyCycle(100)
            pwmRF.ChangeDutyCycle(0)
            pwmLB.ChangeDutyCycle(0)
            pwmRB.ChangeDutyCycle(100)
        # Stop
        if (w == True and s == True) or (a == True and d == True):
            pwmLF.ChangeDutyCycle(0)
            pwmRF.ChangeDutyCycle(0)
            pwmLB.ChangeDutyCycle(0)
            pwmRB.ChangeDutyCycle(0)
        if w == False and s == False and a == False and d == False:
            pwmLF.ChangeDutyCycle(0)
            pwmRF.ChangeDutyCycle(0)
            pwmLB.ChangeDutyCycle(0)
            pwmRB.ChangeDutyCycle(0)

        self.send_response(301)
        self.send_header('Location', '/index.html')
        self.end_headers()

    # send html page to browser with video feed
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

# Define the Streaming Server
class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# Start the Camera and the Webserver
with picamera.PiCamera(resolution='640x480', framerate=32) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 180
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        # Stop the Camera Webserver and GPIO
        camera.stop_recording()
        pwmLF.stop()
        pwmLB.stop()
        pwmRF.stop()
        pwmRB.stop()
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)
        GPIO.output(pin3, GPIO.LOW)
        GPIO.output(pin4, GPIO.LOW)
