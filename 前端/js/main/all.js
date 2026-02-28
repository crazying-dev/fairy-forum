window.addEventListener('wheel', function(e) {
    if (e.ctrlKey) {
        e.preventDefault(); // 阻止默认缩放行为
    }
}, { passive: false }); // passive: false 确保能阻止默认行为

// 禁止双击缩放（部分浏览器生效）
window.addEventListener('dblclick', function(e) {
    e.preventDefault();
});

// 禁止键盘缩放快捷键（Ctrl+/Ctrl-）
window.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && (e.key === '+' || e.key === '-' || e.key === '=')) {
        e.preventDefault();
    }
});