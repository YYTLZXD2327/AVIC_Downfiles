function logoutFunction() {
  fetch('./logout', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => {
      if (response.ok) {
        window.location.href = './login';
      } else {
        console.error('退出登录失败...自己找问题吧');
      }
    })
    .catch(error => {
      console.error('错误:', error);
    });
  return false;
}

const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('uploadButton');

let selectedFile = null;

fileInput.addEventListener('change', function (event) {
  const file = event.target.files[0];
  if (file) {
    selectedFile = file;
    uploadButton.disabled = false;
  }
});

uploadButton.addEventListener('click', function () {
  if (selectedFile) {
    const formData = new FormData();
    formData.append('file', selectedFile);
    fetch('/upload', {
      method: 'POST',
      body: formData
    })
      .then(response => {
        if (response.ok) {
          alert(`文件 |${selectedFile.name}| 上传成功！`);
          selectedFile = null;
          uploadButton.disabled = true;
          location.reload(true);
        } else {
          return response.text().then(errorText => {
            throw new Error(`上传失败: ${errorText}`);
          });
        }
      })
  }
});