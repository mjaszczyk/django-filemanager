try
	jQ = django.jQuery
catch err
	jQ = $

jQ(document).ready ->
	jQ(".insert-button").click(insertButtonClicked)
	if (jQ("#result_list").find("button").length > 0)
		jQ("th a, td a").click (e) ->
            e.preventDefault()
			jQ(this).parents('tr').find("button.insert-button").click()

insertButtonClicked = (evt) ->
	evt.preventDefault()
	window.opener.insertSingleImage(jQ(this).attr("ref"), jQ(this).attr("name"), jQ(this).attr("addr"), window)

insertSingleImage = (id, name, addr, window) ->
	lastAction(id, name, addr, window)
