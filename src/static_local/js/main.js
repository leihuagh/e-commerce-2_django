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
        console.log(data)
      },
      error: function(error) {
        console.log('Error when add to cart => ', error)
      }
    })
    console.log();
  });
});
