function loadJSON(jsonFilePath, callback=null) {
    var xobj = new XMLHttpRequest()
    xobj.overrideMimeType("application/json")
    xobj.open('GET', jsonFilePath, true)
    xobj.onreadystatechange = function () {
      if(xobj.readyState == 4 && xobj.status == "200") {
        callback(xobj.responseText)
      }
      else {
        callback(xobj.readyState + xobj.status)
      }
    }
    xobj.send(null)
}


function showJson(json) {
  document.getElementById('json').innerHTML = json
}

setTimeout(function() {
  loadJSON('/response_text.json', showJson)
}, 2727);
