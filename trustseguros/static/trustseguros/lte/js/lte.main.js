function startLoader() {
    $('#loader').css('display', 'initial')
}

function stopLoader() {
    $('#loader').css('display', 'none')
}

function intcommas(x) {
    x = x.toString();
    let pattern = /(-?\d+)(\d{3})/;
    while (pattern.test(x))
        x = x.replace(pattern, "$1,$2");
    return x;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

$(document).ready(function(){
    const menu = $('a[href="' + $('input[name="path"]').val() + '"]');
    menu.addClass('active');
    menu.parents('.has-treeview').addClass('active').addClass('menu-open');
})
