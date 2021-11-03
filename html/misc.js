window.addEventListener('load', (event) => {
    console.log("on load")
    showSnack(9000)
});

function showSnack(time_ms) {
    //time_ms is time before deleted, not fade_out
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
  
    // Add the "show" class to DIV
    x.className = "show";
  
    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, time_ms);
  }