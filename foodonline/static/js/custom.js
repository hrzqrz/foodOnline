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
               }
               
            }
        })
    })
    // decrease cart end

})