const setIcon = document.getElementById('set');
const setIconB = document.getElementById('set-background')
const setDropList = document.getElementById('set-droplist')
const setDropListSignOut = document.getElementById('sign out')
const setDropListSignIn = document.getElementById('sign in')

const getCookieSimple = (name) => decodeURIComponent(document.cookie.split(`${encodeURIComponent(name)}=`)[1]?.split(';')[0] || '');

let id = getCookieSimple('id');

if (!id || id.toString().trim() === "") {
    setDropListSignOut.style.display = 'none'
} else {
    setDropListSignIn.style.display = 'none'
}

// 动画过渡
setIcon.style.transition = 'all 1.5s ease';
setIconB.style.transition = 'background-color 1.5s ease';
setDropList.style.transition = 'height 1.5s ease';

// 动画
function SetTurnTo(){
    setIcon.style.transform = 'rotate(180deg)';
    setIconB.style.backgroundColor = 'rgba(100,100,100,0.7)'
    setIcon.style.width = '60px'
    setIcon.style.height = '60px'
    setIcon.style.top = '15px'
    setIcon.style.right = '30px'
    setDropList.style.height = setDropList.scrollHeight + 'px'
}

function  SetTurnBreak(){
    setIcon.style.transform = 'rotate(0deg)';
    setIconB.style.backgroundColor = 'rgba(0,0,0,0)'
    setIcon.style.width = '50px'
    setIcon.style.height = '50px'
    setIcon.style.top = '20px'
    setIcon.style.right = '35px'
    setDropList.style.height = '0'
}


// 2. 监听鼠标悬浮事件（mouseover：鼠标进入）
setIconB.addEventListener('mouseover', SetTurnTo);

// 3. 监听鼠标离开事件（mouseout：鼠标离开），恢复初始状态
setIconB.addEventListener('mouseout', SetTurnBreak);

