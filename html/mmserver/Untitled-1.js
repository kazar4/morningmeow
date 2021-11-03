var response = fetch('http://morningmeow.com:3000/secret', 
{
    method: 'GET', // *GET, POST, PUT, DELETE, etc.
    mode: 'no-cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    }}).then(function(response) {
  return response.json();
}).then(function(responseJson) {
  var clientSecret = responseJson.client_secret;
  console.log(clientSecret);
});


var response = fetch('http://morningmeow.com:3000/secret').then(function(response) {
  return response.json();
}).then(function(responseJson) {
  var clientSecret = responseJson.client_secret;
  console.log(clientSecret);
});
