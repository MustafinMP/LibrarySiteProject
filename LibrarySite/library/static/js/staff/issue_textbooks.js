//var app = new Vue({
//  delimiters: ["[[", "]]"],
//  el: '#app',
//  data: {
//    message: 'Hello Vue!'
//  }
//})

let jsVariable = JSON.parse(document.getElementById('djangoData').textContent);

var app = new Vue({
  delimiters: ["[[", "]]"],
  el: '#app',
  data: {
    message: jsVariable
  }
})