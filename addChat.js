var iframe = document.createElement('iframe');

// iframe 스타일 설정
iframe.style.position = 'absolute'; // 절대 위치
iframe.style.right = '20px'; // 왼쪽으로부터 10px 떨어지게 위치
iframe.style.bottom = '20px'; // 아래쪽으로부터 10px 떨어지게 위치
iframe.style.width = '28.125vh'; // 너비
iframe.style.height = '50vh'; // 높이
iframe.style.border = 'none'; // 테두리 제거

var wrapper = document.querySelector('.entryBoardWrapper');

wrapper.appendChild(iframe);

fetch('https://raw.githubusercontent.com/triangle231/chatui/main/chatui.html')
    .then(response => response.text())
    .then(html => {
        var blob = new Blob([html], { type: 'text/html' });
        var url = URL.createObjectURL(blob);
        iframe.src = url;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
