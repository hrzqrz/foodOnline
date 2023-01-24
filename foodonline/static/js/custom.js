$(document).ready(function(){
    // add to cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
      
        $.ajax({
            type: 'GET',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
              },
            url: url,
            success: function(response){
               console.log(response)
               if(response.status == 'login_required'){
                // swal({
                //       title: "Good job!",
                //       text: "You clicked the button!",
                //       icon: "success",
                //     });
                swal(response.message, '', 'info').then(function(){
                   window.location = '/login'; 
                })
               }if(response.status == 'Failed'){
                swal(response.message, '', 'error')
               }else{
                $('#cart_counter').html(response.cart_counter['cart_count'])
                $('#qty-'+food_id).html(response.qty)

                // subtotal, tax and grand total
                applyCartAmounts(
                    response.cart_amount['subtotal'],
                    response.cart_amount['tax'],
                    response.cart_amount['grand_total']
                )
               }
               
            },
        })
    })
    // add to cart  end



    // Place the cart item quantity on load 
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })
    // Place the cart item quantity on load  end


    // decrease cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id')
        $.ajax({
            type: 'GET',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
              },
            url: url,
            success: function(response){
               console.log(response)
               if(response.status == 'login_required'){
                swal(response.message, '', 'info').then(function(){
                    window.location = '/login';
                })
               }else if(response.status == 'Failed'){
                swal(response.message, '', 'error')
               }else{
                $('#cart_counter').html(response.cart_counter['cart_count'])
                $('#qty-'+food_id).html(response.qty)

                // subtotal, tax and grand total
                applyCartAmounts(
                    response.cart_amount['subtotal'],
                    response.cart_amount['tax'],
                    response.cart_amount['grand_total']
                )

                if(window.location.pathname == '/cart/'){
                    removeCartItem(response.qty, cart_id);
                    checkEmptyCart();
                }
               }
               
            }
        })
    })
    // decrease cart end


    // Delete cart items start
    $('.delete_cart').on('click', function(e){
        e.preventDefault();
        // alert('testing');
        // return false;
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        $.ajax({
            type: 'GET',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
              },
            url: url,
            success: function(response){
               console.log(response)
               if(response.status == 'Failed'){
               swal(response.message, '', 'error')
               }else{
                $('#cart_counter').html(response.cart_counter['cart_count'])
                swal(response.status, response.message, 'succes')

                // subtotal, tax and grand total
                applyCartAmounts(
                    response.cart_amount['subtotal'],
                    response.cart_amount['tax'],
                    response.cart_amount['grand_total']
                )
                
                removeCartItem(0, cart_id)
                checkEmptyCart();
               }
               
            }
        })
    })
    // Delete cart items ends

    // Delete the cart element if the qty is 0 start

    function removeCartItem(cartItemQty, cart_id){
        if(cartItemQty <= 0) {
            // Remove the cart item element
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }

    // Delete the cart element if the qty is 0 end

    // Check if the cart is empty starts 

    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter == 0){
            document.getElementById("empty-cart").style.display = "block";
        }
    }

    // Check if the cart is empty ends

    // Apply cart amounts starts

    function applyCartAmounts(subtotal, tax, grand_total){
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grand_total)
        }
        
    }

    // Apply cart amounts ends


})