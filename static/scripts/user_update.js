function auto_grow(element) {
    element.style.height = "6px";
    element.style.height = (element.scrollHeight)+"px";
}
auto_grow(document.querySelector('.form_update textarea'));