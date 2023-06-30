var board = null;
var game = new Chess();
var $status = $("#status");
var $fen = $("#fen");
var $pgn = $("#pgn");
var $oponentuserername = $("#oponentusername");
var whiteSquareGrey = "#a9a9a9";
var blackSquareGrey = "#696969";
var oponentgiveup = false;
var igiveup = false;
var oponentpk = -1;
const usr_id = JSON.parse(document.getElementById("usr_id").textContent);
const roomName = JSON.parse(document.getElementById("room-name").textContent);
const invitorusername = JSON.parse(
  document.getElementById("invitor_username").textContent
);
const invitorcolor = JSON.parse(
  document.getElementById("invitor_color").textContent
);
const username = JSON.parse(document.getElementById("username").textContent);
const pk = JSON.parse(document.getElementById("usr_id").textContent);
if (invitorusername != username)
{
  $oponentuserername.html(invitorusername)
}
else
{
  $oponentuserername.html("oczekiwanie na przeciwnika") 
}

function colorselector(x, y, z) {
  if (z == x) {
    if (y == "black") {
      return "black";
    } else {
      return "white";
    }
  } else {
    if (y == "black") {
      return "white";
    } else {
      return "black";
    }
  }
}

const playercolor = colorselector(username, invitorcolor, invitorusername);

const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/onlinegame/" + roomName + "/"
);

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);

  if (data.message == "joined" && data.fen != game.fen() && data.username != username)
  {
    info()
  }
  if (data.message == "info" && data.fen != game.fen() && username != data.username)
  {
    board.position(data.fen, false)
    game = new Chess(data.fen)
    $pgn.html(data.pgn)
  }

  if ( data.username != username && data.pk != usr_id )
  {
    if (data.username != "")
    {
      $oponentuserername.html(data.username)

    }
    else
    {
      $oponentuserername.html("użytkownik niezalogowany")
    }
    oponentpk = data.pk
  }
  ///$oponentusername.html(data.username);
  OnlineMove(data.from, data.to);
  if (game.pgn() != data.pgn) {
    if (data.pgn.length > game.pgn().length) {
      board.position(data.fen, false);
    }
  }
};

chatSocket.onclose = function (e) {
  console.error("Chat socket closed unexpectedly");
};

function OnlineMove(source, target) {
  game.move({
    from: source,
    to: target,
    promotion: "q",
  });
  board.position(game.fen());
  updateStatus();
}

function removeGreySquares() {
  $("#myBoard .square-55d63").css("background", "");
}

function greySquare(square) {
  var $square = $("#myBoard .square-" + square);

  var background = whiteSquareGrey;
  if ($square.hasClass("black-3c85d")) {
    background = blackSquareGrey;
  }

  $square.css("background", background);
}

function onDragStart(source, piece, position, orientation) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false;

  // only pick up pieces for the side to move
  if (playercolor == "white") {
    if (piece.search(/^b/) !== -1) return false;
  } else {
    if (piece.search(/^w/) !== -1) return false;
  }
}

function onDrop(source, target) {
  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: "q", // NOTE: always promote to a queen for example simplicity
  });

  // illegal move
  if (move === null) return "snapback";

  chatSocket.send(
    JSON.stringify({
      message: "hello",
      from: source,
      to: target,
      fen: game.fen(),
      pgn: game.pgn(),
      pk: pk,
      username: username,
    })
  );

  updateStatus();
}

function onMouseoverSquare(square, piece) {
  // get list of possible moves for this square
  var moves = game.moves({
    square: square,
    verbose: true,
  });

  // exit if there are no moves available for this square
  if (moves.length === 0) return;

  // highlight the square they moused over
  greySquare(square);

  // highlight the possible squares for this piece
  for (var i = 0; i < moves.length; i++) {
    greySquare(moves[i].to);
  }
}

function onMouseoutSquare(square, piece) {
  removeGreySquares();
}

function onSnapEnd() {
  board.position(game.fen());
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd() {
  board.position(game.fen());
}

function surrender(){
  chatSocket.send(JSON.stringify({message: "surrender",from: '',to: '',fen: game.fen(),pgn: game.pgn(),pk: pk,username: username,}));
  igiveup = true;
}

function joined(){
  chatSocket.send(JSON.stringify({message: "joined",from: '',to: '',fen: game.fen(),pgn: game.pgn(),pk: pk,username: username,}));
console.log("joined")
}
function info(){
  chatSocket.send(JSON.stringify({message: "info",from: '',to: '',fen: game.fen(),pgn: game.pgn(),pk: pk,username: username,}));
console.log("info")
}
function updateStatus() {
  var status = "";

  var moveColor = "Białe";
  if (game.turn() == "b") {
    moveColor = "Czarne";
  }

  // checkmate?
  if (game.in_checkmate()) {
    console.log("wygrana")
    status = "Koniec gry, " + moveColor + " są w szachu, przegrały";
    if (moveColor == "Białe")
    {
    $("#id_result").val(1)
    }
    else{
    $("#id_result").val(2)
    }
    $("#hiddenbutton").css("visibility","visible")
    alert(status)
  }

  // draw?
  else if (game.in_draw()) {
    console.log("remis")
    status = "Koniec gry, remis";
    $("#id_pgn").val(game.pgn())
    if(game.in_checkmate() == false )
    {
      $("#id_result").val(3)
    }
    $("#hiddenbutton").css("visibility","visible")
    alert(status)
  }

  // game still on
  else {
    if (moveColor == "Białe") {
      status = "ruch Białych";
    } else {
      status = "ruch Czarnych";
    }

    // check?
    if (game.in_check()) {
      status += ", " + moveColor + " w szachu";
    }

  }
  if (playercolor == "black")
  {
    console.log('wpisz do player2')
    document.getElementById("id_player2").value=usr_id
    document.getElementById("id_player1").value=oponentpk
  }
  else
  {
    console.log('wpisz do player1 ')
    document.getElementById("id_player1").value=usr_id
    document.getElementById("id_player2").value=oponentpk
  }
  $("#id_pgn").val(game.pgn())
  $status.html(status);
  $fen.html(game.fen());
  $pgn.html(game.pgn());
}

if (playercolor == "white") {
  var config = {
    draggable: true,
    position: "start",
    onDragStart: onDragStart,
    onDrop: onDrop,
    onMouseoutSquare: onMouseoutSquare,
    onMouseoverSquare: onMouseoverSquare,
    onSnapEnd: onSnapEnd,
  };
} else {
  var config = {
    draggable: true,
    position: "start",
    orientation: "black",
    onDragStart: onDragStart,
    onDrop: onDrop,
    onMouseoutSquare: onMouseoutSquare,
    onMouseoverSquare: onMouseoverSquare,
    onSnapEnd: onSnapEnd,
  };
}
board = Chessboard("myBoard", config);
updateStatus();
$(window).resize(function () {
  board.resize();
});

setTimeout(() => { joined(); }, 500);