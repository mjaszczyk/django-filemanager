window.init_plupload = (url, success_url) ->
    $ ->
        $('form').submit (e) ->
            uploader = $('#uploader').pluploadQueue()

            if (uploader.files.length > 0)
                uploader.bind('StateChanged', ->
                    if (uploader.files.length == (uploader.total.uploaded + uploader.total.failed))
                        $('form')[0].submit()
                )
                uploader.start()

        uploader = new plupload.Uploader
            browse_button : 'pickfiles',
            container : 'upload-container',
            runtimes : 'html5,gears,flash,silverlight',
            url : url,
            max_file_size : '10mb',
            chunk_size : '1mb',
            unique_names : true,
            flash_swf_url : "#{STATIC_URL}js/plupload/plupload.flash.swf",
            silverlight_xap_url : "#{STATIC_URL}js/plupload/plupload.silverlight.xap",
            headers : {'X-Requested-With' : 'XMLHttpRequest', 'X-CSRFToken' : getCsrfTokenValue()}
            preinit :
                UploadComplete: ->
                    window.location = success_url
                    location.reload true

        $('#uploadfiles').click (e)->
            uploader.start()
            e.preventDefault()

        uploader.init()

        uploader.bind 'FilesAdded', (up, files) ->
            $.each files, (i, file) ->
                $('#filelist').append "<li id='#{file.id}'>#{file.name} (#{plupload.formatSize(file.size)})</li>"
            up.refresh()

        uploader.bind 'UploadProgress', (up, file) ->
            $('#' + file.id + " b").html(file.percent + "%")

        uploader.bind 'Error', (up, err) ->
            $('#filelist').append("<div>Error: " + err.code +
                ", Message: " + err.message + "</div>"
            )
            up.refresh()

        uploader.bind 'FileUploaded', (up, file) ->
            $('#' + file.id + " b").html("100%")
