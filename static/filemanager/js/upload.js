
  window.init_plupload = function(url, success_url) {
    return $(function() {
      var uploader;
      uploader = $("#uploader").pluploadQueue({
        runtimes: 'html5,gears,flash,silverlight',
        url: url,
        max_file_size: '10mb',
        chunk_size: '1mb',
        unique_names: true,
        resize: {
          width: 320,
          height: 240,
          quality: 90
        },
        flash_swf_url: "" + STATIC_URL + "js/plupload/plupload.flash.swf",
        silverlight_xap_url: "" + STATIC_URL + "js/plupload/plupload.silverlight.xap",
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCsrfTokenValue()
        },
        preinit: {
          UploadComplete: function() {
            window.location = success_url;
            return location.reload(true);
          }
        }
      });
      return $('form').submit(function(e) {
        uploader = $('#uploader').pluploadQueue();
        if (uploader.files.length > 0) {
          uploader.bind('StateChanged', function() {
            if (uploader.files.length === (uploader.total.uploaded + uploader.total.failed)) {
              return $('form')[0].submit();
            }
          });
          return uploader.start();
        }
      });
    });
  };
