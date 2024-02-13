var lutDisplay = document.querySelector('.last-update-time')
const lastUpdateTime = "2024年2月13日"

function refreshPage() {
  location.reload(true);
}

lutDisplay.innerHTML = `最后提交时间：<i class="fa-solid fa-check"></i>${lastUpdateTime}`;

function logoutFunction() {
  fetch('/logout', {
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