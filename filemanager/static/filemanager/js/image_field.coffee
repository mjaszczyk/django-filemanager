try
	jQ = django.jQuery
catch err
	jQ = $

try
	a = inputToInsertTo
catch err
	inputToInsertTo = null

try
	b = lastAction
catch err
	lastAction = null

try
	c = insertSingleImage
catch err
	insertSingleImage = (id, name, addr, window) ->
		lastAction(id, name, addr, window)

jQ(document).ready ->
	el = jQ(".input-insert-image")
	el.next(".add-another").remove()
	el.click(insertClicked)
	jQ(".remove-image").click(removeClicked)
	
removeClicked = (e) ->
	e.preventDefault()
	$(this).prev().fadeOut(100).prev().fadeOut(100).prev().val("")
	$(this).fadeOut(100)

insertClicked = (evt) ->
    href = POPUP_ADDR
    if REPLACE_IN_POPUP_ADDR
        href = href.replace "??", REPLACE_IN_POPUP_ADDR
    
    FBWindow = window.open(href,
        String("Obrazy"),
    'height=600,width=960,resizable=yes,scrollbars=yes')
    inputToInsertTo = jQ(this).parent().find("input").attr("id")
    FBWindow.focus()
    lastAction = insertToSingleInputImage
    evt.preventDefault()

window.insertSingleImage = (id, name, addr, window) ->
	lastAction(id, name, addr, window)

insertToSingleInputImage = (id, name, addr, window) ->
    el = jQ("#" + inputToInsertTo)
    el.val(id)
    el.next('.image-name').text(name).fadeIn(100)
        .next().attr("src", addr).show(100)
        .next().show(100)
    window.close()
