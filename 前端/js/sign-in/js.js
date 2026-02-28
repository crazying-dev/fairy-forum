const Btn = document.getElementById('loginBtn')
const error_password = document.getElementById('error-password')
const error_password_none = document.getElementById('error-password-none')
const error_name_none = document.getElementById('error-name-none')
const error_name = document.getElementById('error-name')
const error_password_length = document.getElementById('error-password-length')

// 优化1：统一隐藏所有错误提示（原仅隐藏了error_password）
const allErrorElements = [error_password, error_password_none, error_name_none, error_name, error_password_length];
allErrorElements.forEach(el => {
    if (el) el.style.display = 'none'; // 增加元素存在性判断，避免报错
});

function hasSpecialChar(password) {
    return !/^[a-zA-Z0-9]+$/.test(password);
}

function isStringEmpty(str) {
    if (str === null || str === undefined) {
        return true;
    }
    if (typeof str !== 'string') {
        return true;
    }
    return str.trim() === '';
}

/**
 * 判断传入的字符串是否只包含：数字、字母、下划线、多语言文字（中文/韩文/日文等）
 * @param {string | null | undefined} str - 要判断的字符串（允许null/undefined）
 * @returns {boolean} - true=仅含允许的字符，false=包含其他字符（或为空/非字符串）
 */
function onlyHasNumLetterUnderline(str) {
    if (str === null || str === undefined || typeof str !== 'string') {
        return false;
    }
    const pureStr = str.trim();
    if (pureStr === '') {
        return false;
    }
    // 核心修改：正则匹配多语言文字 + 数字 + 字母 + 下划线
    // \p{L} 匹配所有Unicode语言字符（包含中文、韩文、日文、英文、俄文等所有语言的文字）
    // [0-9_] 匹配数字和下划线
    // u 修饰符：启用Unicode模式，支持\p{L}
    const reg = /^[\p{L}0-9_]+$/u;
    return reg.test(pureStr);
}

// 优化2：增强showThenHideAfter5s，防止重复点击导致定时器叠加
function showThenHideAfter5s(target, showDisplay = 'block') {
    let element;
    if (typeof target === 'string') {
        element = document.getElementById(target);
    } else if (target instanceof HTMLElement) {
        element = target;
    }

    if (!element) {
        console.warn('目标元素不存在！');
        return;
    }

    // 新增：清除该元素的旧定时器，避免多次点击叠加
    if (element.timer) clearTimeout(element.timer);

    element.style.display = showDisplay;
    // 存储定时器ID到元素属性
    element.timer = setTimeout(() => {
        element.style.display = 'none';
        delete element.timer; // 执行后清除ID
    }, 5000);
}

function isLengthBetween8And12(str, trim = true) {
    if (str === null || str === undefined || typeof str !== 'string') {
        return false;
    }
    const pureStr = trim ? str.trim() : str;
    const length = pureStr.length;
    return length >= 8 && length <= 12;
}

function send(name, password){
    // 服务器通讯的位置
}

function click(){
    // 优化3：获取输入值后立即去除首尾空格（核心！避免空格导致校验误判）
    let name = document.getElementById("name").value.trim();
    let password = document.getElementById("password").value.trim();
    let turn = true

    if (isStringEmpty(name)){
        showThenHideAfter5s(error_name_none)
        turn = false;
    }
    else if (!onlyHasNumLetterUnderline(name)){
        showThenHideAfter5s(error_name)
        turn = false;
    }

    if (isStringEmpty(password)){
        showThenHideAfter5s(error_password_none)
        turn = false;
    }
    else if (hasSpecialChar(password)){
        showThenHideAfter5s(error_password)
        turn = false;
    }
    else if (!isLengthBetween8And12(password)){
        showThenHideAfter5s(error_password_length)
        turn = false;
    }

    if (!turn){
        return false
    }

    send(name, password)
}

Btn.addEventListener('click', click)
// 可选优化：密码框按回车键触发登录（提升体验）
const passwordInput = document.getElementById('password');
if (passwordInput) {
    passwordInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') click();
    });
}