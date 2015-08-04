(function(){


  $('#requested_slug').keyup(function() {
    var slug = $(this).val();
    if (slug.length > 0) {
      checkRequestedSlug($(this).val());
    }
    else {
      $('.slug-form-group').removeClass('available').removeClass('taken');
      $('.taken-url').html('');
    }
  });

  $('#url-form').submit(function(event) {
    event.preventDefault();
    var data = $(this).serialize();
    $.ajax({
      url: "api/",
      type: "POST",
      data: data,
      success: function(response) {
        $('#form').addClass('fade-away');
        $('#results').addClass('fade-in');
        $('#result_url').val(location.host + '/' + response + '/');
        $('#result_url').select();
      },
      error: function(xhr) {

      }
    });
    
  });

  function checkRequestedSlug(slug) {
    $.ajax({
      url: "api/",
      type: "get",
      data:{slug: slug},
      success: function(response) {
        if (response.length < 1) {
          $('.slug-form-group').addClass('available').removeClass('taken');
          $('.taken-url').html('');
        } else {
          $('.slug-form-group').removeClass('available').addClass('taken');
          $('.taken-url').html('<a href="' + response + '" target="_blank">' + response + '</a>');
        }

      },
      error: function(xhr) {

      }
    });
    
  }

    


  // Taken from Django docs on passing CSRF token with AJAX.
  // https://docs.djangoproject.com/en/1.8/ref/csrf/
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  $(document).ready(function() {

    $(function() {
      $.ajaxSetup({
          headers: {
              "X-CSRFToken": getCookie("csrftoken")
          }
        });
    });

  });
})();