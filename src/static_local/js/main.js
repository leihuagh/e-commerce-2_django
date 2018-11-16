$(document).ready(() => {
  const productForm = $(".form-product-ajax");
  productForm.submit(function(e) {
    e.preventDefault();
    // console.log(e.target.attributes.action.value);
    // console.log(e.target.attributes.method.value);
    // console.log(e.target.product_id.value);
    
    const thisForm = $(this);
    const actionEndpoint = thisForm.attr("action");
    const httpMethod = thisForm.attr("method");
    const formData = thisForm.serialize()
    console.log(productForm, thisForm, actionEndpoint, httpMethod, formData);

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data) {
        const submitSpan = thisForm.find('.submit-span')
        if (data.added) {
          submitSpan.html('In cart <button type="submit" class="btn btn-link">Remove</button>')
        } else {
          submitSpan.html('<button type="submit" class="btn btn-success">Add to cart</button>')
        }
        const navbarCartCount = $('.navbar-cart-count')
        navbarCartCount.text(data.cartItemCount)
      },
      error: function(error) {
        console.log('Error when add to cart => ', error)
      }
    })
    console.log();
  });
});
