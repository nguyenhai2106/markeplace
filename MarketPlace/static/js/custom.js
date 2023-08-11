// noinspection DuplicatedCode
let modalFooter = $("#modalFooter")
$(document).ready(function () {
    $('#myOrdersTable').DataTable({
        "lengthChange": false
    });

    $('.add_to_cart').on('click', function (e) {
        e.preventDefault();
        let food_id = $(this).attr('data-id');
        let data_url = $(this).attr('data-url')
        let cart_id = $(this).attr('cart-id');
        $.ajax({
            type: "GET",
            url: data_url,
        }).done(function (response) {
            if (response.status == 'login_required') {
                if (modalFooter.find(".btn-login").length === 0) {
                    let link = $("<a></a>");
                    link.attr("href", "/login");
                    link.addClass("btn btn-primary btn-login");
                    link.text("Đăng Nhập");
                    modalFooter.prepend(link);
                }
                show_alert_modal(response.message)
            } else if (response.status == 'Failed') {
                show_alert_modal(response.message)
            } else {
                $('#cart_counter').html(response.cart_counter['cart_count'])
                $('#cart_counter').removeClass("bg-primary p-2").addClass("bg-danger")
                $('#input-qty-' + food_id).val(response.quantity)
                $('#sub_cart_item-' + cart_id).text(response.subtotal_of_item)
                set_cart_amounts(response.cart_amounts.subtotal, response.cart_amounts.tax, response.cart_amounts.total)
            }
        })
    })

    $('.decrease_cart').on('click', function (e) {
        e.preventDefault();
        let food_id = $(this).attr('data-id');
        let data_url = $(this).attr('data-url');
        let cart_id = $(this).attr('cart-id');
        $.ajax({
            type: "GET",
            url: data_url,
        }).done(function (response) {
            if (response.status == 'login_required') {
                if (modalFooter.find(".btn-login").length === 0) {
                    let link = $("<a></a>");
                    link.attr("href", "/login");
                    link.addClass("btn btn-primary btn-login");
                    link.text("Đăng Nhập");
                    modalFooter.prepend(link);
                }
                show_alert_modal(response.message)
            } else if (response.status == 'Failed') {
                show_alert_modal(response.message)
            } else {
                if (response.cart_counter['cart_count'] < 1) {
                    $('#cart_counter').removeClass("bg-danger").addClass("bg-primary p-2")
                    $('#cart_counter').html("<span class=\"visually-hidden\">New alerts</span>")
                    $('#cart_status').removeClass('d-none')
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                }
                $('#input-qty-' + food_id).val(response.quantity)
                $('#sub_cart_item-' + cart_id).text(response.subtotal_of_item)
                if (response.quantity < 1) {
                    removeCartItemWithZeroQuantity(response.quantity, cart_id, "Món ăn '" + response.food_name + "' đã được xóa khỏi giỏ hàng!")
                }
                set_cart_amounts(response.cart_amounts.subtotal, response.cart_amounts.tax, response.cart_amounts.total)

            }
        })
    })


    $('.delete_cart_item').on('click', function (e) {
        e.preventDefault();
        let cart_id = $(this).attr('data-id');
        let data_url = $(this).attr('data-url')
        $.ajax({
            type: "GET",
            url: data_url,
        }).done(function (response) {
            if (response.status == 'Failed') {
                show_alert_modal(response.message)
            } else {
                if (response.cart_counter['cart_count'] < 1) {
                    $('#cart_counter').removeClass("bg-danger").addClass("bg-primary p-2")
                    $('#cart_counter').html("<span class=\"visually-hidden\">New alerts</span>")
                    $('#cart_status').removeClass('d-none')
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                }
                removeCartItemWithZeroQuantity(0, cart_id, response.message);
                set_cart_amounts(response.cart_amounts.subtotal, response.cart_amounts.tax, response.cart_amounts.total)
            }
        })
    })


    $('.item_qty').each(function () {
        let food_id = $(this).attr('id');
        let quantity = $(this).attr('data-quantity')
        $('#input-' + food_id).val(quantity)
    });
})

function show_alert_modal(content) {
    $("#modal-content").html(content);
    $("#alert-modal").modal('show');
}

function removeCartItemWithZeroQuantity(quantity, cart_id, message) {
    if (quantity <= 0) {
        $("#cart_item-" + cart_id).remove()
        show_alert_modal(message)
    }
}

function set_cart_amounts(subtotal, tax, total) {
    $("#subtotal").text(subtotal);
    $("#tax").text(tax);
    $("#total").text(total);
}

function payment_method_confirm() {
    let payment_method = $("input[name='payment_method']:checked").val()
    if (!payment_method) {
        show_alert_modal("Vui lòng chọn phương thức thanh toán!");
        return false;
    } else {
        if (modalFooter.find(".btn-submit").length === 0) {
            let link = $("<a></a>");
            link.attr("href", "#");
            link.addClass("btn btn-primary btn-submit");
            link.text("Xác nhận");
            modalFooter.prepend(link);
        }
        show_alert_modal("Bạn xác nhận thanh toán bằng " + payment_method);
        $(".btn-submit").on('click', function () {
            $("#checkout_form").submit()
        })
    }
    return false;
}