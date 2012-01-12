(function() {
  var a, b, c, inputToInsertTo, insertClicked, insertSingleImage, insertToSingleInputImage, jQ, lastAction, removeClicked;

  try {
    jQ = django.jQuery;
  } catch (err) {
    jQ = $;
  }

  try {
    a = inputToInsertTo;
  } catch (err) {
    inputToInsertTo = null;
  }

  try {
    b = lastAction;
  } catch (err) {
    lastAction = null;
  }

  try {
    c = insertSingleImage;
  } catch (err) {
    insertSingleImage = function(id, name, addr, window) {
      return lastAction(id, name, addr, window);
    };
  }

  jQ(document).ready(function() {
    var el;
    el = jQ(".input-insert-image");
    el.next(".add-another").remove();
    el.click(insertClicked);
    return jQ(".remove-image").click(removeClicked);
  });

  removeClicked = function(e) {
    e.preventDefault();
    $(this).prev().fadeOut(100).prev().fadeOut(100).prev().val("");
    return $(this).fadeOut(100);
  };

  insertClicked = function(evt) {
    var FBWindow, href;
    href = '/filemanager/staticfile/popuplist/image/';
    FBWindow = window.open(href, String("Obrazy"), 'height=600,width=960,resizable=yes,scrollbars=yes');
    inputToInsertTo = jQ(this).parent().find("input").attr("id");
    FBWindow.focus();
    lastAction = insertToSingleInputImage;
    return evt.preventDefault();
  };

  window.insertSingleImage = function(id, name, addr, window) {
    return lastAction(id, name, addr, window);
  };

  insertToSingleInputImage = function(id, name, addr, window) {
    var el;
    el = jQ("#" + inputToInsertTo);
    el.val(id);
    el.next('.image-name').text(name).fadeIn(100).next().attr("src", addr).show(100).next().show(100);
    return window.close();
  };

}).call(this);
