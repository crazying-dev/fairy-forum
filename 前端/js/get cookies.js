const getCookieSimple = (name) => decodeURIComponent(document.cookie.split(`${encodeURIComponent(name)}=`)[1]?.split(';')[0] || '');

// 使用示例
const age = getCookieSimple('age');
console.log(age); // 输出：18