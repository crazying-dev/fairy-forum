const head_user_Img = document.getElementById('user-img')
const head_user_Imgbackground = document.getElementById('user-background')

head_user_Imgbackground.style.transition = 'all 0.5s ease'
head_user_Img.style.transition = 'all 0.5s ease'

const head_user_getCookieSimple = (name) => decodeURIComponent(document.cookie.split(`${encodeURIComponent(name)}=`)[1]?.split(';')[0] || '');

let head_user_id = head_user_getCookieSimple('id');
console.log(head_user_getCookieSimple('id'));
// 核心判断逻辑
if (!head_user_id || head_user_id.toString().trim() === "") {
    head_user_Img.src = 'https://raw.githubusercontent.com/crazying-dev/other/main/use/break/user-img.png'
    // 后期论坛封闭后改为跳转登陆页面
    //window.location.href = "/sign-in.html"
} else if (!/^\d+$/.test(id.toString().trim())) {
    window.location.href = "/sign-in";
} else {
    // true
}

function INTO(){
    head_user_Imgbackground.style.backgroundColor = 'rgba(100,100,100,0.7)'
    head_user_Img.style.top = '20px'
    head_user_Img.style.right = '195px'
    head_user_Img.style.height = '60px'
    head_user_Img.style.width = '60px'
}

function OUT() {
    head_user_Imgbackground.style.backgroundColor = 'rgba(0,0,0,0)'
    head_user_Img.style.top = '25px'
    head_user_Img.style.right = '200px'
    head_user_Img.style.height = '50px'
    head_user_Img.style.width = '50px'
}


head_user_Imgbackground.addEventListener('mouseover', INTO)
head_user_Imgbackground.addEventListener('mouseout', OUT)