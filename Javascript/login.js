
var login_user = function() {
  var request = new XMLHttpRequest();
  request.open("POST", "http://localhost:8080/sessions")
  request.onreadystatechange = function() {
    if(request.readyState == XMLHttpRequest.DONE) {
      if(request.status >= 200 && request.status < 400) {
        var data = JSON.parse(request.responseText)
        window.alert("Welcome " + data.f_name + " " + data.l_name + "!");
        //hide the login stuff
        login_form.style.display = 'none';
        getPokemon();
      } else {
        window.alert("Invalid email/password");
      }
    }
  };

  var login_form = document.getElementById("login-form");
  var content = document.getElementById('content-container');
  var welcome = document.getElementById('welcome');

  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;
  request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  request.withCredentials = true;
  request.send("email="+encodeURIComponent(email)+"&password="+encodeURIComponent(password));
};

var loginButton = document.getElementById("login");
loginButton.onclick = function() {
  login_user();
};

var createPokemon = function(values, success, failure) {
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if (request.readyState == XMLHttpRequest.DONE) {
			if(request.status >= 200 && request.status <400) {
        getPokemon();
        //location.reload();
			} else {
        //do nothing
			}
		}
	};

	var name = document.getElementById("name").value;
	var gender = document.getElementById("gender").value;
	var type = document.getElementById("type").value;
	var size = document.getElementById("size").value;
	var strength = document.getElementById("strength").value;
	var weakness = document.getElementById("weakness").value;

	request.open("POST", "http://localhost:8080/pokemon");
	request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  request.withCredentials = true;
	request.send("name="+encodeURIComponent(name)+"&gender="+encodeURIComponent(gender)+
			"&type="+encodeURIComponent(type)+"&size="+encodeURIComponent(size)+
			"&strength="+encodeURIComponent(strength)+"&weakness="+encodeURIComponent(weakness));
};

var submitButton = document.getElementById("submit_button");
submitButton.onclick = function () {
	createPokemon(name, function () {
		console.log("Pokemon created!");
	}, function () {
		console.error("Unable to create pokemon.");
	});
};

var getPokemon = function() {
	var getRequest = new XMLHttpRequest();
	getRequest.onreadystatechange = function() {
		if(getRequest.readyState == XMLHttpRequest.DONE) {
			if(getRequest.status >= 200 && getRequest.status < 400) {
				//console.log(getRequest.responseText);
				var pokemon = JSON.parse(getRequest.responseText)
				//console.log(pokemon);
        // Display pokedex table
        content.style.display = 'block';
        // Hide login form
        login_form.style.display = 'none';
        // Set title
        title.getElementsByTagName("h4")[0].innerHTML = "Pokedex";
        // remove trs with class name of pokemon-row
        removeElementsByClass("pokemon-row");
        //Make table row add pokemon
				for(item in pokemon) {
					addPokemon(item, pokemon[item]);
				}
			} else {
			//do nothing
			}
		}
	};
  var trs = document.getElementsByClassName("pokemon-row");
  var table = document.getElementById("t-body");
  var content = document.getElementById("content-container");
  content.style.display = 'none';
  var login_form = document.getElementById("login-form");
  var title = document.getElementById('title');

	getRequest.open("GET", "http://localhost:8080/pokemon");
  getRequest.withCredentials = true;
	getRequest.send();
};

var removeElementsByClass = function(className) {
  var elements = document.getElementsByClassName(className);
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
};

var addPokemon = function (item, pokemon) {
  var table = document.getElementById("t-body");
  var t_r = document.createElement("tr");
  t_r.className = "pokemon-row";
  table.appendChild(t_r);

	// Attribute: ID
	var td_id = document.createElement("td");
	td_id.value = pokemon.id;
	td_id.innerHTML = pokemon.id;
	t_r.appendChild(td_id);
	// Attribute: Name
	var td_name = document.createElement("td");
	td_name.innerHTML = pokemon.name;
	t_r.appendChild(td_name);
	// Attribute: Gender
	var td_gender = document.createElement("td");
	td_gender.innerHTML = pokemon.gender;
	t_r.appendChild(td_gender);
	// Attribute: Type
	var td_type = document.createElement("td");
	td_type.innerHTML = pokemon.type;
	t_r.appendChild(td_type);
	// Attribute: Size
	var td_size = document.createElement("td");
	td_size.innerHTML = pokemon.size;
	t_r.appendChild(td_size);
	// Attribute: Strength
	var td_strength = document.createElement("td");
	td_strength.innerHTML = pokemon.strength;
	t_r.appendChild(td_strength);
	// Attribute: Weakness
	var td_weakness = document.createElement("td");
	td_weakness.innerHTML = pokemon.weakness;
	t_r.appendChild(td_weakness);

	// Edit button
	var td_editBtn = document.createElement("td");
	var editBtn = document.createElement("button");
	editBtn.id = "t-edit";
	editBtn.type = "submit";
	var l = document.createTextNode("Edit");
	editBtn.appendChild(l);
	td_editBtn.appendChild(editBtn);
	t_r.appendChild(td_editBtn);

	// Delete Buton
	var td_deleteBtn = document.createElement("td");
	var deleteBtn = document.createElement("button");
	deleteBtn.type = "submit";
	var l = document.createTextNode("Delete");
	deleteBtn.appendChild(l);
	td_deleteBtn.appendChild(deleteBtn);
	t_r.appendChild(td_deleteBtn);

	deleteBtn.onclick = function (event) {
		//event.preventDefault();
		var r = window.confirm("Are you sure you want to DELETE this Pokemon?");
		if(r == true) {
			to_delete_pokemon(td_id, function () {
				console.log("item id deleted", pokemon.id);
			}, function () {
				console.error("Unable to delete pokemon.")
			});
		} else {
  		//event.preventDefault();
		}
	};

	var modal = document.getElementById('myModal');
	var span = document.getElementById('close');

	var m_name = document.getElementById('m-name');
	var m_gender = document.getElementById('m-gender');
	var m_type = document.getElementById('m-type');
	var m_size = document.getElementById('m-size');
	var m_strength = document.getElementById('m-strength');
	var m_weakness = document.getElementById('m-weakness');

	editBtn.onclick = function (event) {

		event.preventDefault();
		modal.style.display = "block";

		//Pre-fill form
		m_name.value = pokemon.name;
		m_gender.value = pokemon.gender;
		m_type.value = pokemon.type;
		m_size.value = pokemon.size;
		m_strength.value = pokemon.strength;
		m_weakness.value = pokemon.weakness;

		var id = pokemon.id;

		var m_edit = document.getElementById('edit_button');


		m_edit.onclick = function () {
			event.preventDefault();
			var r = window.confirm("Are you sure you want to Edit this pokemon?");
			if(r == true) {
				to_edit_pokemon(id);
				modal.style.display = "none";
			} else {
				event.preventDefault();
			}
		};
	};

	span.onclick = function() {
		modal.style.display = "none"
	};

	window.onclick = function(event) {
		if(event.target == modal) {
			modal.style.display = "none";
		}
	}
};

var to_delete_pokemon = function (id, success, failure) {
	//console.log(id.value);
	var deleteRequest = new XMLHttpRequest();
		deleteRequest.onreadystatechange = function () {
		if (deleteRequest.readyState == XMLHttpRequest.DONE) {
			if(deleteRequest.status >= 200 && deleteRequest.status < 400) {
				var json = JSON.parse(deleteRequest.responseText);
				console.log(json);
				console.log(json.id);
        getPokemon();
        //location.reload();
			}
		}
	};

	var params = id.value;
  deleteRequest.open("DELETE", "http://localhost:8080/pokemon/" + params);
  deleteRequest.withCredentials = true;
	deleteRequest.setRequestHeader("content-type", "application/x-www-form-urlencoded");
	deleteRequest.send();
};

var to_edit_pokemon = function (id) {
	var updateRequest = new XMLHttpRequest();
  updateRequest.open("PUT", "http://localhost:8080/pokemon/"+id);
	updateRequest.onreadystatechange = function () {
		if(updateRequest.readyState == XMLHttpRequest.DONE) {
			if(updateRequest.status >= 200 && updateRequest.status < 400) {
				console.log(updateRequest.responseText);
        console.log('update');
        getPokemon();
        //location.reload();
			}
		}
	};
	var name = document.getElementById("m-name").value;
	var gender = document.getElementById("m-gender").value;
	var type = document.getElementById("m-type").value;
	var size = document.getElementById("m-size").value;
	var strength = document.getElementById("m-strength").value;
	var weakness = document.getElementById("m-weakness").value;

	updateRequest.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  updateRequest.withCredentials = true;
	updateRequest.send("name="+encodeURIComponent(name)+"&gender="+encodeURIComponent(gender)+
			"&type="+encodeURIComponent(type)+"&size="+encodeURIComponent(size)+
			"&strength="+encodeURIComponent(strength)+"&weakness="+encodeURIComponent(weakness));
};

getPokemon();
