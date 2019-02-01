$(document).ready(() => {
  const productForm = $(".form-product-ajax");
  
  function getOwnedProduct(productId, submitSpan){
    const actionEndpoint = '/orders/endpoint/verify/ownership/'
    const httpMethod = 'GET'
    const data = {
      product_id: productId
    }
    let isOwner;

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: data,
      success: function(data){
        if (data.owner){
          isOwner = true
          submitSpan.html("<a class='btn btn-warning' href='/orders/library/'>In Library</a>");
        } else {
          isOwner = false
        }
      },
      error: function(error){
        console.log("Error when verifiying ownership => ", error);
      }
    })
    return isOwner
  }

  $.each(productForm, function(index, object){
    const $this = $(this);
    const isUser = $this.attr("data-user");
    const submitSpan = $this.find(".submit-span");
    const productInput = $this.find("[name='product_id']");
    const productId = productInput.attr("value");
    const productIsDigital = productInput.attr("data-is-digital");
    
    if (productIsDigital && isUser){
      const isOwned = getOwnedProduct(productId, submitSpan) 
    }
  })  

  
  productForm.submit(function(e) {
    e.preventDefault();
    const thisForm = $(this);
    // const actionEndpoint = thisForm.attr("action");
    const actionEndpoint = thisForm.attr("data-endpoint");
    const httpMethod = thisForm.attr("method");
    const formData = thisForm.serialize();

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data) {
        const submitSpan = thisForm.find(".submit-span");
        if (data.added) {
          submitSpan.html(
            // '<a href='/cart/'>In cart</a> <button type="submit" class="btn btn-link">Remove</button>'
            `<div class='btn-group'>
              <a class='btn btn-link' href='/cart/'>In cart</a> 
              <button type="submit" class="btn btn-link">Remove</button>
            </div>`
          );
        } else {
          submitSpan.html(
            '<button type="submit" class="btn btn-success">Add to cart</button>'
          );
        }
        const navbarCartCount = $(".navbar-cart-count");
        navbarCartCount.text(data.cartItemCount);
        const currentPath = window.location.href;
        if (currentPath.indexOf("cart") != -1) {
          refreshCart();
        }
      },
      error: function(error) {
        $.alert({
          title: "Oops!",
          content: "An error occurred",
          theme: "modern"
        });
        console.log("Error when add to cart => ", error);
      }
    });
  });

  function refreshCart() {
    const cartTable = $(".cart-table");
    const cartBody = cartTable.find(".cart-body");
    const productRows = cartBody.find(".cart-product");
    const currentUrl = window.location.href;
    const refreshCartUrl = "/cart-api/";
    const refreshCartMethod = "GET";
    const data = {};
    $.ajax({
      url: refreshCartUrl,
      method: refreshCartMethod,
      data: data,
      success: function(data) {
        const hiddenCartItemRemoveForm = $(".cart-item-remove-form");
        if (data.products.length > 0) {
          productRows.html(" ");
          let i = data.products.length;
          $.each(data.products, (index, product) => {
            const newCartItemRemove = hiddenCartItemRemoveForm.clone();
            newCartItemRemove.css("display", "block");
            newCartItemRemove.find(".cart-item-product-id").val(product.id);
            cartBody.prepend(`<tr>
                              <th scope="row">${i}</th>
                                <td>
                                  <a href="${product.url}">${product.name}</a> 
                                  <br>
                                  <small>
                                    ${newCartItemRemove.html()}
                                  </small>
                                </td>
                                <td>${product.price}</td>
                              </tr>`);
            i--;
          });
          cartBody.find(".cart-subtotal").text(data.subtotal);
          cartBody.find(".cart-total").text(data.total);
        } else {
          window.location.href = currentUrl;
        }
      },
      error: function(error) {
        $.alert({
          title: "Oops!",
          content: "An error occurred",
          theme: "modern"
        });
        console.log("Error when refresh cart => ", error);
      }
    });
  }
});
