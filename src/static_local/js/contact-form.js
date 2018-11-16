$(document).ready(() => {
  const contactForm = $(".contact-form");
  const contactFormMethod = contactForm.attr("method");
  const contactFormEndpoint = contactForm.attr("action");

  contactForm.submit(function(e) {
    e.preventDefault();
    const contactFormData = contactForm.serialize();
    // const thisForm = $(this);
    $.ajax({
      url: contactFormEndpoint,
      method: contactFormMethod,
      data: contactFormData,
      success: function(data) {
        // thisForm[0].reset();
        contactForm[0].reset();
        console.log(data)
        $.alert({
          title: "Success!",
          content: data.message,
          theme: "supervan"
        });
      },
      error: function(error) {
        $.alert({
          title: "Oops!",
          content: "An error occurred",
          theme: "modern"
        });
        console.log("Error when saving contact form => ", error);
      }
    });
  });
});
