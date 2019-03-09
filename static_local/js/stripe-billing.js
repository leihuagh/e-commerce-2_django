$(document).ready(function() {
  var stripeFormModule = $(".stripe-payment-form");
  var stripeModuleToken = stripeFormModule.attr("data-token");
  var stripeModuleNextUrl = stripeFormModule.attr("data-next-url");
  var stripeModuleCreate = stripeFormModule.attr("data-create");
  var stripeModuleBtnTitle = stripeFormModule.attr('data-btn-title') || 'Add Card'

  var stripeTemplate = $.templates("#stripeTemplate");
  var stripeTemplateDataContext = {
    publishKey: stripeModuleToken,
    nextUrl: stripeModuleNextUrl,
    create: stripeModuleCreate,
    btnTitle: stripeModuleBtnTitle
  };
  var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext);
  stripeFormModule.html(stripeTemplateHtml);

  var paymentForm = $(".payment-form");

  if (paymentForm.length > 1) {
    alert("Only one payment form is allowed per page");
    paymentForm.css("display", "none");
  } else if (paymentForm.length == 1) {
    var pubKey = paymentForm.attr("data-token");
    var paymentMethodEndpoint = paymentForm.attr("data-create");
    var nextUrl = paymentForm.attr("data-next-url");










    

    // Create a Stripe client.
    var stripe = Stripe(pubKey);

    // Create an instance of Elements.
    var elements = stripe.elements();

    // Custom styling can be passed to options when creating an Element.
    // (Note that this demo uses a wider set of styles than the guide below.)
    var style = {
      base: {
        color: "#32325d",
        lineHeight: "18px",
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: "antialiased",
        fontSize: "16px",
        "::placeholder": {
          color: "#aab7c4"
        }
      },
      invalid: {
        color: "#fa755a",
        iconColor: "#fa755a"
      }
    };

    // Create an instance of the card Element.
    var card = elements.create("card", { style: style });

    // Add an instance of the card Element into the `card-element` <div>.
    card.mount("#card-element");

    // Handle real-time validation errors from the card Element.
    card.addEventListener("change", function(event) {
      var displayError = document.getElementById("card-errors");
      if (event.error) {
        displayError.textContent = event.error.message;
      } else {
        displayError.textContent = "";
      }
    });

    // // Handle form submission.
    // var form = document.getElementById("payment-form");
    // form.addEventListener("submit", function(event) {
    //   event.preventDefault();

    //   stripe.createToken(card).then(function(result) {
    //     if (result.error) {
    //       // Inform the user if there was an error.
    //       var errorElement = document.getElementById("card-errors");
    //       errorElement.textContent = result.error.message;
    //     } else {
    //       // Send the token to your server.
    //       stripeTokenHandler(nextUrl, result.token);
    //     }
    //   });
    // });


    // Handle form submission.
    var form = $("#payment-form");
    var btnLoad = form.find('.btn-load');
    var btnLoadDefaultHtml = btnLoad.html();
    var btnLoadDefaultClasses = btnLoad.attr("class");

    form.on("submit", function(event) {
      event.preventDefault();

      var $this = $(this);
      btnLoad.blur();
      var loadTime = 1500;
      var currentTimeout;
      var errorHtml = "<i class='fa fa-warning'></i> An error occurred";
      var errorClasses = "btn btn-danger disabled my-3";
      var loadingHtml = "<i class='fa fa-spin fa-spinner'></i> Loading...";
      var loadingClasses = "btn btn-success disabled my-3";

      stripe.createToken(card).then(function(result) {
        if (result.error) {
          // Inform the user if there was an error.
          var errorElement = $("#card-errors");
          errorElement.textContent = result.error.message;
          currentTimeout = displayBtnStatus(btnLoad, errorHtml, errorClasses, 1000, currentTimeout);
        } else {
          // Send the token to your server.
          currentTimeout = displayBtnStatus(btnLoad, loadingHtml, loadingClasses, 10000, currentTimeout);
          stripeTokenHandler(nextUrl, result.token);
        }
      });
    });

    function displayBtnStatus(element, newHtml, newClasses, loadTime, timeout){
      if (!loadTime){
        loadTime = 1500;
      }
      element.html(newHtml);
      element.removeClass(btnLoadDefaultClasses);
      element.addClass(newClasses);
      return setTimeout(function(){
          element.html(btnLoadDefaultHtml);
          element.removeClass(newClasses);
          element.addClass(btnLoadDefaultClasses);
      }, loadTime);
    }

    // Submit the form with the token ID.
    function stripeTokenHandler(nextUrl, token) {
      // Insert the token ID into the form so it gets submitted to the server
      var form = document.getElementById("payment-form");
      var hiddenInput = document.createElement("input");
      hiddenInput.setAttribute("type", "hidden");
      hiddenInput.setAttribute("name", "stripeToken");
      hiddenInput.setAttribute("value", token.id);
      form.appendChild(hiddenInput);

      // Submit the form
      // form.submit();












      // var paymentMethodEndpoint = '/billing/payment-method/create/'
      var data = {
        token: token.id
      };
      $.ajax({
        data: data,
        url: paymentMethodEndpoint,
        method: "POST",
        success: function(data) {
          var successMsg =
            data.message || "Success! Your cart was added successfully!";
          card.clear();
          if (nextUrl) {
            successMsg =
              successMsg +
              '<br><br><i class="fa fa-spin fa-spinner"></i> Redirecting...';
          }
          if ($.alert) {
            $.alert(successMsg);
          } else {
            alert(successMsg);
          }
          btnLoad.html(btnLoadDefaultHtml);
          btnLoad.attr('class', btnLoadDefaultClasses);
          redirectToNext(nextUrl, 1500);
        },
        error: function(error) {
          console.log("Error while creating new payment method", error);
          $.alert({title: "An error occured", content: "Please try to add your card again."});
          btnLoad.html(btnLoadDefaultHtml);
          btnLoad.attr('class', btnLoadDefaultClasses);
        }
      });
    }

    function redirectToNext(nextPath, timeOffset) {
      if (nextPath) {
        setTimeout(function() {
          window.location.href = nextPath;
        }, timeOffset);
      }
    }
  }
});
