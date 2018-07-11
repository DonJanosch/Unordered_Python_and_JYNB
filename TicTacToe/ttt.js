// Restart Game
var restart = document.querySelector("#btn_restart");
restart.addEventListener('click',clearBoard);

// Graps all the squares
var squares = document.querySelectorAll("td");

// Clear all the squares
function clearBoard(){
for (var i=0;i<squares.length;i++){
squares[i].textContent = "";
}
}

// Function to toggle through the markers
function changeMarker(){
switch (this.textContent){

case '':
this.textContent = 'X';
break;

case 'X':
this.textContent = 'O';
break;

default:
this.textContent = '';
}
}

// Apply it to every td-cell
for (var i = 0; i <squares.length; i++){
squares[i].addEventListener("click",changeMarker)
}