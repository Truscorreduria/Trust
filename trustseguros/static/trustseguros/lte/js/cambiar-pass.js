$(document).ready(function(){
    const passmodal = $('#modal-cambiar-pass').iziModal({
            headerColor: '#326634'
        })
    $(document).on('click', '#btn-cambiar-pass', function(){
        const _this = $(this);

        console.log(_this)
        passmodal.iziModal('open')
    })
})