function minus(e) {
    var id_data = new FormData();
    var id = e.target.id

    id_data.append('minus', id)

        $.ajax({
            type: 'POST',
            url: '/forms/cart/quantity',
            data: id_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function() {
                location.reload();
            },
        });
}

function plus(e) {
    var id_data = new FormData();
    var id = e.target.id

    id_data.append('plus', id)

        $.ajax({
            type: 'POST',
            url: '/forms/cart/quantity',
            data: id_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function() {
                location.reload();
            },
        });
}

function remove(e) {
    var id_data = new FormData();
    var id = e.target.id

    id_data.append('remove', id)

    $.ajax({
        type: 'POST',
        url: '/forms/cart/remove',
        data: id_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function() {
            location.reload();
        },
    });
}

$('.radio-group .radio').click(function(){
    $('.radio').addClass('gray');
    $(this).removeClass('gray');
});