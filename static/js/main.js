const startBtn = document.getElementById('startBtn');
const output = document.getElementById('output');
const op=document.getElementById('stop');
const val=document.getElementById('wid');
const clear=document.getElementById('clear');

clear.addEventListener('click',function(){
    val.value="";
})

// Check if browser supports SpeechRecognition
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    // Set properties for recognition
    recognition.lang = 'en-US';
    recognition.interimResults = true;
    recognition.continuous = true;

    // Event listener for speech recognition results
    recognition.onresult = function(event) {
        const result = event.results[event.resultIndex];
        const transcript = result[0].transcript;
        output.textContent = transcript;
        val.value=transcript;
    };

    // Event listener for errors
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
    };

    // Event listener for when speech recognition starts
    recognition.onstart = function() {
        val.value = 'Listening...';
    };

    // Event listener for when speech recognition ends
    recognition.onend = function() {
        output.textContent = 'Speech recognition ended.';
    };

    // Event listener for the start button
    startBtn.addEventListener('click', function() {
        recognition.start();
        console.log("muninender");
    });
    
    op.addEventListener('click',function(){
        recognition.stop();
    });
    
} else {
    output.textContent = 'Speech recognition not supported in this browser.';
}

function loadVideoSource() {
    fetch('/video_path') // Endpoint to get the video path
        .then(response => response.json())
        .then(data => {
            const video = document.getElementById('assistant-video');
            video.src = data.video_path;
        })
        .catch(error => console.error('Error loading video source:', error));
}

// Example using fetch API
fetch('/video_path')
    .then(response => response.json())
    .then(data => {
        const videoPath = data.video_path;
        document.getElementById('assistant-video').src = videoPath;
    })
    .catch(error => console.error('Error fetching video path:', error));


// Call loadVideoSource function after the page loads
window.onload = loadVideoSource;

