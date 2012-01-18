window.init_plupload = (url, success_url) ->
    $ ->
        uploader = $("#uploader").pluploadQueue
            runtimes : 'html5,gears,flash,silverlight',
            url : url,
            max_file_size : '10mb',
            chunk_size : '1mb',
            unique_names : true,
            resize : {width : 320, height : 240, quality : 90},
            flash_swf_url : "#{STATIC_URL}js/plupload/plupload.flash.swf",
            silverlight_xap_url : "#{STATIC_URL}js/plupload/plupload.silverlight.xap",
            headers : {'X-Requested-With' : 'XMLHttpRequest', 'X-CSRFToken' : getCsrfTokenValue()}
            preinit :
                     UploadComplete: ->
                        window.location = success_url
                        location.reload true
                        
                          

        $('form').submit (e) ->
            uploader = $('#uploader').pluploadQueue()

            if (uploader.files.length > 0)
                uploader.bind('StateChanged', ->
                    if (uploader.files.length == (uploader.total.uploaded + uploader.total.failed))
                        $('form')[0].submit()
                )
                uploader.start()
