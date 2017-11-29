
var create_user = function(values) {
  var request = new XMLHttpRequest();
  request.open("POST", "http://localhost:8080/users");
  request.withCredentials = true;
  request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

  if(document.getElementById("f_name").value != '') {
    var f_name = document.getElementById("f_name").value;
  }
  if(document.getElementById("l_name").value != '') {
    var l_name = document.getElementById("l_name").value;
  }
  if(document.getElementById("email").value != '') {
    var email = document.getElementById("email").value;
  }
  if(document.getElementById("password").value != '') {
    var password = document.getElementById("password").value;

  }
  else {
    console.log("error");
  }

  request.onreadystatechange = function() {
    if (request.readyState == XMLHttpRequest.DONE) {
      if(request.status >= 200 && request.status < 400) {
        //call functions?
        //success();
        //login_user();
        window.alert("Registration was succuessful!");
      } else {
        window.alert("Error: Invalid email/password. Please try again.");
        //failure();
      }
    }
  };

  request.send("f_name="+encodeURIComponent(f_name)+"&l_name="+encodeURIComponent(l_name)+
    "&email="+encodeURIComponent(email)+"&password="+encodeURIComponent(password));
};

var email = document.getElementById("email").value;
var register_button = document.getElementById("register");
register_button.onclick = function () {
  create_user(email);
};

var login_user = function() {
  var request = new XMLHttpRequest();
  request.open("POST", "http://localhost:8080/sessions")
  request.onreadystatechange = function() {
    if(request.readyState == XMLHttpRequest.DONE) {
      if(request.status >= 200 && request.status < 400) {
        //something
        window.alert("user was logged in");
      } else {
        //seomthing
      }
    }
  };
  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;
  request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  request.withCredentials = true;
  request.send("email="+encodeURIComponent(email)+"&password="+encodeURIComponent(password));
};

var loginButton = document.getElementById("login");
loginButton.style.display = 'none';
loginButton.onclick = function() {
  login_user();
};
