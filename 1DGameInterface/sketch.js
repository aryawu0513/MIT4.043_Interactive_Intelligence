/* /////////////////////////////////////

  4.043 / 4.044 Design Studio: Interaction Intelligence
  February 9, 2024
  Marcelo Coelho

*/ /////////////////////////////////////

let displaySize = 30; // how many pixels are visible in the game
let pixelSize = 20; // how big each 'pixel' looks on screen

let playerOne; // Adding 2 players to the game
let playerTwo;
let target; // and one target for players to catch.

let display; // Aggregates our final visual output before showing it on the screen

let controller; // This is where the state machine and game logic lives

let collisionAnimation; // Where we store and manage the collision animation

let score; // Where we keep track of score and winner

let ground = [];

function setup() {
  createCanvas(displaySize * pixelSize, pixelSize); // dynamically sets canvas size

  for (let i = 0; i < displaySize; i++) {
    // Randomly assign ground or void
    ground[i] = random() < 0.8 ? "GROUND" : "VOID";
  }

  display = new Display(displaySize, pixelSize, ground); //Initializing the display
  display.setGround(ground);
  //console.log(ground);
  playerOne = new Player(color(255, 0, 0), parseInt(3), displaySize); // Initializing players
  playerTwo = new Player(color(0, 0, 255), parseInt(0), displaySize);

  tangleAnimation = new Animation(); // Initializing animation
  breakAnimation = new Animation();

  controller = new Controller(); // Initializing controller

  //score = { max: 3, winner: color(0, 0, 0) }; // score stores max number of points, and color
}

function draw() {
  // start with a blank screen
  background(0, 0, 0);

  // Runs state machine at determined framerate
  controller.update();

  // After we've updated our states, we show the current one
  display.show();
}
