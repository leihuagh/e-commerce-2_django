$(document).ready(() => {
  const productForm = $(".form-product-ajax");
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
            'In cart <button type="submit" class="btn btn-link">Remove</button>'
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
        console.log("Error when add to cart => ", error);
      }
    });
  });
  console.log();

  function refreshCart() {
    const cartTable = $(".cart-table");
    const cartBody = cartTable.find(".cart-body");
    // cartBody.html("<h1>changed</h1>");
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
        console.log("Error when refresh cart => ", error);
      }
    });
  }
});
