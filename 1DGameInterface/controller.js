// This is where your state machines and game logic lives

class Controller {
  // This is the state we start with.
  constructor() {
    this.gameState = "START";
    this.startTime = 0;
    this.endTime = 0;
    this.totalTime = 0;
  }

  // This is called from draw() in sketch.js with every frame
  update() {
    this.checkDistance();
    this.checkVoid();
    // STATE MACHINE ////////////////////////////////////////////////
    // This is where your game logic lives
    /////////////////////////////////////////////////////////////////
    switch (this.gameState) {
      case "START":
        // clear screen at frame rate so we always start fresh
        display.clear();
        for (let i = 0; i < displaySize; i++) {
          // Randomly assign ground or void
          ground[i] = random() < 0.8 ? "GROUND" : "VOID";
        }
        ground[0] = ground[3] = "GROUND";
        display.setGround(ground);
        playerOne.position = 3;
        playerOne.level = 0;
        playerTwo.position = 0;
        playerTwo.level = 0;
        this.startTime = millis();
        this.endTime = 0;
        this.totalTime = 0;
        this.gameState = "PLAY";

      // This is the main game state, where the playing actually happens
      case "PLAY":
        // clear screen at frame rate so we always start fresh
        display.clear();

        display.setGround(ground);
        //console.log(ground);

        // show all players in the right place, by adding them to display buffer
        display.setPixel(playerOne.position, playerOne.playerColor);
        display.setPixel(playerTwo.position, playerTwo.playerColor);
        // Add ground and void pixels to display buffer
        if (playerOne.level === 3 && playerTwo.level === 3) {
          this.gameState = "WIN";
          console.log("Both players at level 3. WIN ");
          this.endTime = millis();
        }
        break;
      case "FAR": //case FAR
        // clear screen at frame rate so we always start fresh
        display.clear();

        // play explosion animation one frame at a time.
        // first figure out what frame to show
        let frameToShow1 = breakAnimation.currentFrame(); // this grabs number of current frame and increments it

        // then grab every pixel of frame and put it into the display buffer
        for (let i = 0; i < breakAnimation.pixels; i++) {
          display.setPixel(i, breakAnimation.animation[frameToShow1][i]);
        }

        //check if animation is done and we should move on to another state
        if (frameToShow1 == breakAnimation.animation.length - 1) {
          this.gameState = "PLAY";
          playerOne.position = 3;
          playerOne.level = 0;
          playerTwo.position = 0;
          playerTwo.level = 0;
        }
        this.startTime = millis();
        break;
      // This state is used to play an animation, after a target has been caught by a player
      case "CLOSE": //case CLOSE
        // clear screen at frame rate so we always start fresh
        display.clear();

        // play explosion animation one frame at a time.
        // first figure out what frame to show
        let frameToShow2 = tangleAnimation.currentFrame(); // this grabs number of current frame and increments it

        // then grab every pixel of frame and put it into the display buffer
        for (let i = 0; i < tangleAnimation.pixels; i++) {
          display.setPixel(i, tangleAnimation.animation[frameToShow2][i]);
        }

        //check if animation is done and we should move on to another state
        if (frameToShow2 == tangleAnimation.animation.length - 1) {
          this.gameState = "PLAY";
          playerOne.position = 3;
          playerOne.level = 0;
          playerTwo.position = 0;
          playerTwo.level = 0;
        }
        this.startTime = millis();
        break;

      // Game is over. Show winner and clean everything up so we can start a new game.
      case "WIN":
        //light up w/ winner color by populating all pixels in buffer with their color
        display.clear();
        display.setAllPixels(playerOne.playerColor);
        this.totalTime = (this.endTime - this.startTime) / 1000;
        break;

      // Not used, it's here just for code compliance
      default:
        break;
    }
  }

  checkDistance() {
    let playerOneTotalPosition =
      playerOne.position + playerOne.level * displaySize;
    //console.log("one:" + playerOneTotalPosition);
    let playerTwoTotalPosition =
      playerTwo.position + playerTwo.level * displaySize;
    //console.log("two:" + playerTwoTotalPosition);
    let distance = abs(playerOneTotalPosition - playerTwoTotalPosition);
    //console.log(distance);

    let requiredDistance = 3 - min(playerOne.level, playerTwo.level);
    let halfDisplaySize = displaySize / 2; // Assuming displaySize is even

    if (distance < requiredDistance) {
      console.log("Players are too close!");

      // Play animation for too close
      this.gameState = "CLOSE";
    } else if (distance > halfDisplaySize) {
      console.log("Players are too far!");
      this.gameState = "FAR";
    }
  }

  checkVoid() {
    if (ground[playerOne.position] === "VOID" && keyPressedFlag === false) {
      console.log("PlayerOne dies");
      // Add any additional actions you want to take when player loses
    }
    if (ground[playerTwo.position] === "VOID" && keyPressedFlag === false) {
      console.log("PlayerTwo dies");
      // Add any additional actions you want to take when player loses
    }
  }
}
let keyPressedFlag = false;

// This function gets called when a key on the keyboard is pressed
function keyPressed() {
  keyPressedFlag = true;
  //Move player one to the left if letter A is pressed
  // if (key == "A" || key == "a") {
  //   playerTwo.move(-1);
  // }

  // And so on...
  if (key == "D" || key == "d") {
    playerTwo.move(1);
  }

  // if (key == "J" || key == "j") {
  //   playerOne.move(-1);
  // }

  if (key == "L" || key == "l") {
    playerOne.move(1);
  }

  // When you press the letter R, the game resets back to the play state
  if (key == "R" || key == "r") {
    controller.gameState = "START";
  }

  if (key == "S" || key == "s") {
    playerTwo.startDash(); // Start dashing for playerTwo
  }

  if (key == "K" || key == "k") {
    playerOne.startDash(); // Start dashing for playerOne
  }
}

function keyReleased() {
  keyPressedFlag = false;
  if (key == "S" || key == "s") {
    playerTwo.stopDash(); // Stop dashing for playerTwo
  }

  if (key == "K" || key == "k") {
    playerOne.stopDash(); // Stop dashing for playerOne
  }
}
