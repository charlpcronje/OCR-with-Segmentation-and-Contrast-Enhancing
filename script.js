// script.js

const dropZone = document.getElementById('drop-zone');
const message = document.getElementById('message');
const terminal = document.getElementById('terminal');
const output = document.getElementById('output');

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  message.style.opacity = '1';
});

dropZone.addEventListener('dragleave', () => {
  message.style.opacity = '0.5';
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  message.style.display = 'none';
  terminal.classList.add('active');

  const files = e.dataTransfer.files;
  if (files.length > 0) {
    uploadFile(files[0]);
  }
});

function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  const xhr = new XMLHttpRequest();

  xhr.open('POST', '/upload', true);

  xhr.upload.onprogress = function (e) {
    if (e.lengthComputable) {
      const percentComplete = (e.loaded / e.total) * 100;
      output.innerText = `Uploading: ${Math.round(percentComplete)}%`;
    }
  };

  xhr.onload = function () {
    if (xhr.status === 200) {
      // Start receiving logs
      const response = JSON.parse(xhr.responseText);
      if (response.task_id) {
        getLogs(response.task_id);
      } else {
        output.innerText = 'Error: No task ID received.';
      }
    } else {
      output.innerText = 'Error uploading file.';
    }
  };

  xhr.send(formData);
}

function getLogs(taskId) {
  const eventSource = new EventSource(`/logs?task_id=${taskId}`);

  eventSource.onmessage = function (e) {
    output.innerText += e.data + '\n';
    output.scrollTop = output.scrollHeight;
  };

  eventSource.onerror = function () {
    eventSource.close();
    terminal.classList.add('expanded');
  };
}
