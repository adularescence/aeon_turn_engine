const readline = require('readline');

const turn_engine = (n) => {
  // 'Global' Vars
  const num_players = n;
  const deck = ['Nemesis', 'Nemesis'];
  const revealed_deck = [];
  let turn_cycles = 1;

  let key_press;
  const reveal_key = 'r';

  // Helper Functions

  // shamelessly copied code
  const shuffle = (array) => {
    var currentIndex = array.length, temporaryValue, randomIndex;
  
    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
  
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;
  
      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }
  
    return array;
  }

  const ordinal = (n) => {
    const s = ['th', 'st', 'nd', 'rd'], v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  }

  // Xaxos
  // Lash

  // 'Main'

  // Setup
  if (num_players === 2) {
    deck.push('Player 1', 'Player 1', 'Player 2', 'Player 2');
  } else if (num_players === 3) {
    deck.push('Player 1', 'Player 2', 'Player 3', 'Wild');
  } else if (num_players === 4) {
    deck.push('Player 1', 'Player 2', 'Player 3', 'Player 4');
  } else {
    console.log(`Bad number of players: ${num_players} (may or may not even bet a number).`);
  }
  
  // Turn Cycle
  while (1) {
    key_press = readline();
    if (key_press === reveal_key) {
      console.log(`The drawn cards are: [${revealed_deck.join('] [')}]`);
    } else {
      console.log(`The next turn belongs to [${revealed_deck.push(deck.pop())}]`);
      if (deck.length() === 0) {
        console.log(`The turn order deck has been exhausted. Shuffling the revealed turn order deck into the turn order deck.`);
        deck = shuffle(revealed_deck);
        revealed_deck = [];
        print(`This is the ${ordinal(turn_cycles)} set of turns.`);
        turn_cycles++;
      }
    }
  }
}

console.log(process.argv[0]);
turn_engine(process.argv[1]);