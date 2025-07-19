let tokenClient;
let accessToken = null;

function handleCredentialResponse(response) {
  const payload = JSON.parse(atob(response.credential.split('.')[1]));
  document.location.href = 'upload.html?token=' + response.credential;
}

window.onload = () => {
  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get('token');
  if (token && window.location.pathname.endsWith('upload.html')) {
    initApp(token);
  }
};

function initApp(credential) {
  accessToken = credential;
  const payload = JSON.parse(atob(credential.split('.')[1]));
  document.getElementById('user-info').innerHTML = `
    <img src="${payload.picture}" alt="Avatar">
    Olá, ${payload.name}
  `;
  document.getElementById('logout-btn').onclick = () => {
    google.accounts.id.disableAutoSelect();
    location.href = 'index.html';
  };
  initUpload();
}

function initUpload() {
  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('file-input');
  const fileList = document.getElementById('file-list');

  dropZone.addEventListener('dragover', e => e.preventDefault());
  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
  });
  fileInput.addEventListener('change', e => handleFiles(e.target.files));

  function handleFiles(files) {
    fileList.innerHTML = '';
    Array.from(files).forEach((file, idx, arr) => {
      const li = document.createElement('li');
      li.textContent = file.name;
      const progress = document.createElement('progress');
      progress.value = 0; progress.max = 100;
      li.append(progress);
      fileList.append(li);
      uploadFile(file, idx + 1, arr.length, progress);
    });
  }
}

function uploadFile(file, current, total, progressElem) {
  const boundary = '-------314159265358979323846';
  const delimiter = "\r\n--" + boundary + "\r\n";
  const close_delim = "\r\n--" + boundary + "--";
  const metadata = {
    name: file.name,
    mimeType: file.type || 'application/octet-stream'
  };
  const reader = new FileReader();
  reader.onload = e => {
    const contentType = file.type || 'application/octet-stream';
    const base64Data = btoa(e.target.result);
    const multipartRequestBody =
      delimiter +
      'Content-Type: application/json; charset=UTF-8\r\n\r\n' +
      JSON.stringify(metadata) +
      delimiter +
      'Content-Type: ' + contentType + '\r\n' +
      'Content-Transfer-Encoding: base64\r\n' +
      '\r\n' +
      base64Data +
      close_delim;
    fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + accessToken,
        'Content-Type': 'multipart/related; boundary=' + boundary
      },
      body: multipartRequestBody
    })
    .then(res => res.json())
    .then(fileMeta => {
      progressElem.value = 100;
      const link = document.createElement('a');
      link.href = `https://drive.google.com/file/d/${fileMeta.id}/view`;
      link.textContent = 'Abrir no Drive';
      progressElem.parentNode.append(link);
    })
    .catch(console.error);
  };
  reader.readAsBinaryString(file);
}
