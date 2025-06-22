// UI and webcam logic
const uploadBtn = document.getElementById('mode-upload-btn');
const liveBtn = document.getElementById('mode-live-btn');
const captureBtn = document.getElementById('mode-capture-btn');
const uploadView = document.getElementById('upload-view');
const webcamView = document.getElementById('webcam-view');
const liveScanButton = document.getElementById('live-scan-btn');
const captureButton = document.getElementById('capture-btn');
const video = document.getElementById('webcam-feed');
const imagePreview = document.getElementById('image-preview');
let stream;

function setActive(btn) {
  [uploadBtn, liveBtn, captureBtn].forEach(b => b.classList.remove('mode-active', 'text-gray-500'));
  btn.classList.add('mode-active');
}

async function startCamera() {
  if (stream) return;
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
  } catch (err) {
    alert('Unable to access camera: ' + err.message);
  }
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(t => t.stop());
    stream = null;
  }
}

uploadBtn.addEventListener('click', () => {
  setActive(uploadBtn);
  uploadView.classList.remove('hidden');
  webcamView.classList.add('hidden');
  liveScanButton.classList.add('hidden');
  captureButton.classList.add('hidden');
  stopCamera();
});

liveBtn.addEventListener('click', async () => {
  setActive(liveBtn);
  uploadView.classList.add('hidden');
  webcamView.classList.remove('hidden');
  liveScanButton.classList.remove('hidden');
  captureButton.classList.add('hidden');
  await startCamera();
});

captureBtn.addEventListener('click', async () => {
  setActive(captureBtn);
  uploadView.classList.add('hidden');
  webcamView.classList.remove('hidden');
  liveScanButton.classList.add('hidden');
  captureButton.classList.remove('hidden');
  await startCamera();
});

captureButton.addEventListener('click', () => {
  if (!stream) return;
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
  imagePreview.src = canvas.toDataURL('image/png');
});

// enable copy of details
const copyBtn = document.getElementById('copy-btn');
copyBtn.addEventListener('click', () => {
  const details = document.getElementById('output-display').innerText;
  navigator.clipboard.writeText(details);
});

