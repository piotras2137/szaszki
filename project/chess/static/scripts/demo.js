var board = null;
var game = new Chess();

function makeRandomMove() {
  var possibleMoves = game.moves();

  // exit if the game is over
  if (game.game_over()) return;

  var randomIdx = Math.floor(Math.random() * possibleMoves.length);
  game.move(possibleMoves[randomIdx]);
  board.position(game.fen());

  window.setTimeout(makeRandomMove, 500);
}

var config = {
  position : "start",
}
board = Chessboard("myBoard", config);

$(window).resize(function() {
  board.resize()
});

window.setTimeout(makeRandomMove, 500);