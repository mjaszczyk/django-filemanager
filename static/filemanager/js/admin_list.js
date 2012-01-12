(function() {
  var insertButtonClicked, insertSingleImage, jQ;

  try {
    jQ = django.jQuery;
  } catch (err) {
    jQ = $;
  }

  jQ(document).ready(function() {
    jQ(".insert-button").click(insertButtonClicked);
    if (jQ("#result_list").find("button").length > 0) {
      jQ("th a, td a").click(function(e) {
        return e.preventDefault();
      });
      return jQ(this).parents('tr').find("button.insert-button").click();
    }
  });

  insertButtonClicked = function(evt) {
    evt.preventDefault();
    return window.opener.insertSingleImage(jQ(this).attr("ref"), jQ(this).attr("name"), jQ(this).attr("addr"), window);
  };

  insertSingleImage = function(id, name, addr, window) {
    return lastAction(id, name, addr, window);
  };

}).call(this);
