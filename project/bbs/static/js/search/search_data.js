<!--搜索框中输入文字自动触发,并返回对应的信息-->
function _search(value) {
    let cookies = document.cookie.split(',');
    let li = document.getElementById("info");
    let search = document.getElementById("search");
    let html = "";

    let pattern = /csrftoken=(.*)/m;
    let csrf;
    for (let j = 0; j < cookies.length; j++) {
        if (pattern.test(cookies[j])) {
            csrf = pattern.exec(cookies[j])[1];
        }
    }
    li.hidden = !search.value;
    $.ajax({
            type: "post",
            url: "/search/",
            dataType:"json",
            headers:{
                "X-CSRFToken": csrf
            },
            data: "value="+encodeURIComponent(value.trim()),

            success: function (data) {
                if (data["data"].length !== 0) {
                    for (let i = 0; i < data["data"].length; i++) {
                        html += "<li class='list-group-item'><a href=/course/"+ data["data"][i]["id"] + ">" + data["data"][i]["name"] + "</a></li>";
                    }
                } else {
                    html = "<li class='list-group-item'>没有找到对应信息</li>";
                }
                li.innerHTML = html;

            },
        }
    );
}
