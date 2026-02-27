const Img = document.getElementById('user-img')

const getCookieSimple = (name) => decodeURIComponent(document.cookie.split(`${encodeURIComponent(name)}=`)[1]?.split(';')[0] || '');

let id = getCookieSimple('id');
console.log(getCookieSimple('id'));
// 核心判断逻辑
if (!id || id.toString().trim() === "") {
    Img.src = 'assets/image/user-img.png'
    // 后期论坛封闭后改为跳转登陆页面
    //window.location.href = "/sign-in.html"
} else if (!/^\d+$/.test(id.toString().trim())) {
    window.location.href = "/sign-in";
} else {
    // true
}
