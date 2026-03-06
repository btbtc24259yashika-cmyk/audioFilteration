let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");

const snrDisplay = document.getElementById("snr");
const originalRms = document.getElementById("originalRms");
const cleanedRms = document.getElementById("cleanedRms");
const noiseRms = document.getElementById("noiseRms");
const sampleRate = document.getElementById("sampleRate");

const audioPlayer = document.getElementById("audioPlayer");
const graph = document.getElementById("graph");
const status = document.getElementById("status");


stopBtn.disabled = true;


// ---------- RECORD ----------

recordBtn.onclick = async () => {

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);

    audioChunks = [];

    mediaRecorder.ondataavailable = e => {
        audioChunks.push(e.data);
    };

    mediaRecorder.onstop = sendToServer;

    mediaRecorder.start();

    recordBtn.disabled = true;
    stopBtn.disabled = false;

    status.innerText = "Recording...";
};


// ---------- STOP ----------

stopBtn.onclick = () => {

    mediaRecorder.stop();

    recordBtn.disabled = false;
    stopBtn.disabled = true;

    status.innerText = "Processing...";
};


// ---------- SEND ----------

async function sendToServer() {

    const blob = new Blob(audioChunks, { type: "audio/webm" });

    const formData = new FormData();
    formData.append("audio", blob);

    const response = await fetch("/process", {
        method: "POST",
        body: formData
    });

    const result = await response.json();

    console.log("SERVER RESULT:", result);   // ⭐ DEBUG

    if (result.success) {

        snrDisplay.innerText = result.snr + " dB";

        originalRms.innerText = result.original_rms ?? "--";
        cleanedRms.innerText = result.cleaned_rms ?? "--";
        noiseRms.innerText = result.noise_rms ?? "--";
        sampleRate.innerText = result.sample_rate ?? "--";

        graph.src = result.graph + "?t=" + Date.now();
        audioPlayer.src = result.audio + "?t=" + Date.now();

        audioPlayer.load();

        status.innerText = "Done";
    }
    else {
        status.innerText = "Error";
        console.log(result.error);
    }
}