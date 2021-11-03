var image = document.getElementById('dailyImage');
var image_source = document.getElementById('source');

String.prototype.format = function() {
    var s = this,
        i = arguments.length;
    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

$.get("https://morningmeow.com:5000/dailyImage", function(data, status){
    //alert("Data: " + data + "\nStatus: " + status);
    //console.log(data)
    if (status == "success") {
        data_array = data.split("|")
        image_day = data_array[0]
        source_text = data_array[1]

        image.innerHTML = `<img src="https://morningmeow.com/MCI/` + image_day + `.jpg"><img>`;
        image_source.innerHTML = source_text;

    } else {
        image.innerHTML = "There was an error loading the daily image"
    }
});