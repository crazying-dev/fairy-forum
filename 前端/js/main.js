const setIcon = document.getElementById('set');
const setIconB = document.getElementById('set-background')

// 动画过渡
setIcon.style.transition = 'all 1.5s ease';
setIconB.style.transition = 'background-color 1.5s ease';

// 动画
function SetTurnTo(){
    setIcon.style.transform = 'rotate(180deg)';
    setIconB.style.backgroundColor = 'rgba(100,100,100,0.7)'
    setIcon.style.width = '40px'
    setIcon.style.height = '40px'
    setIcon.style.top = '0px'
    setIcon.style.right = '20px'
}

function  SetTurnBreak(){
    setIcon.style.transform = 'rotate(0deg)';
    setIconB.style.backgroundColor = 'rgba(0,0,0,0)'
    setIcon.style.width = '30px'
    setIcon.style.height = '30px'
    setIcon.style.top = '5px'
    setIcon.style.right = '25px'
}


// 2. 监听鼠标悬浮事件（mouseover：鼠标进入）
setIcon.addEventListener('mouseover', SetTurnTo);

// 3. 监听鼠标离开事件（mouseout：鼠标离开），恢复初始状态
setIcon.addEventListener('mouseout', SetTurnBreak);

