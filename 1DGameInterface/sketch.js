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

// let collisionAnimation; // Where we store and manage the collision animation
let fallAnimation;

let score; // Where we keep track of score and winner

let ground = [];

let sound;

function preload() {
  // Load the sound file during preload
  sound = loadSound("robotsound.mp3");
  deathsound = loadSound("videogame-death-sound-43894.mp3");
  //console.log(sound);
}

function setup() {
  frameRate(60);
  //createCanvas(displaySize * pixelSize, pixelSize); // dynamically sets canvas size
  createCanvas(displaySize * pixelSize, 5 * pixelSize);
  for (let i = 0; i < displaySize; i++) {
    // Randomly assign ground or void
    ground[i] = random() < 0.8 ? "GROUND" : "VOID";
  }
  ground[0] = ground[3] = "GROUND";

  display = new Display(displaySize, pixelSize, ground); //Initializing the display
  display.setGround(ground);
  //console.log(ground);
  playerOne = new Player(color(255, 0, 0), parseInt(3), displaySize); // Initializing players
  playerTwo = new Player(color(0, 0, 255), parseInt(0), displaySize);

  display.setGradientColors(3, 0, color(255, 0, 0), color(0, 0, 255));
  tangleAnimation = new closeAnimation(); // Initializing animation
  breakAnimation = new farAnimation();
  fallAnimationOne = new FallOne(playerOne, playerTwo, display);
  fallAnimationTwo = new FallTwo(playerOne, playerTwo, display);
  controller = new Controller(); // Initializing controller

  //score = { max: 3, winner: color(0, 0, 0) }; // score stores max number of points, and color
}

function draw() {
  // start with a blank screen
  background(51, 51, 51);

  // Runs state machine at determined framerate
  controller.update();

  // After we've updated our states, we show the current one
  display.show();
}
