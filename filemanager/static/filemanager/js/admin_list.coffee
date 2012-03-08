jQ = django.jQuery
jQ(document).ready ->
    jQ(".insert-button").click insertButtonClicked
    if jQ("#result_list").find("button").length > 0
        jQ("th a, td a").click (e) ->
            e.preventDefault()
            jQ(this).parents('tr').find("button.insert-button").click()

insertButtonClicked = (evt) ->
    evt.preventDefault()
    if window.opener.lastAction? and window.opener.lastAction
        window.opener.lastAction(jQ(this).attr("ref"), jQ(this).attr("name"), jQ(this).attr("addr"), window)
        window.opener.lastAction = no
    else
        window.opener.insertSingleImage(jQ(this).attr("ref"), jQ(this).attr("name"), jQ(this).attr("addr"), window)

insertSingleImage = (id, name, addr, window) ->
	lastAction(id, name, addr, window)
