function logout() {
    // 注销登录
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            location.reload();
        }
    };
    xhr.open('GET', "/user/logout", true);
    xhr.send();
}
