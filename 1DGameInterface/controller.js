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
          ground[i] = random() < 0.88 ? "GROUND" : "VOID";
        }
        ground[0] = ground[3] = "GROUND";
        //display.setGround(ground);
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
        display.setGradientColors(
          playerOne.position,
          playerTwo.position,
          playerOne.playerColor,
          playerTwo.playerColor
        );
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
          this.gameState = "START";
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
          this.gameState = "START";
          playerOne.position = 3;
          playerOne.level = 0;
          playerTwo.position = 0;
          playerTwo.level = 0;
        }
        this.startTime = millis();
        break;

      // Game is over. Show winner and clean everything up so we can start a new game.
      case "WIN":
        sound.stop();
        //light up w/ winner color by populating all pixels in buffer with their color
        display.clear();
        display.setAllPixels(color(255, 0, 255));
        this.totalTime = (this.endTime - this.startTime) / 1000;
        break;

      case "DeathOne":
        // display.fadeAway(playerOne.position);
        // for (let i = playerTwo.position; i < playerOne.position; i++) {
        //   display.fadeAway(i);
        // }
        // this.gameState = "START";
        // break;
        if (!this.fallAnimationOne) {
          this.fallAnimationOne = new FallOne(playerOne, playerTwo, display);
        }

        let frameToShow3 = this.fallAnimationOne.currentFrame(); // Get the current frame

        // Update the display buffer with the current frame of the animation
        for (let i = 0; i < this.fallAnimationOne.pixels; i++) {
          display.setPixel(i, this.fallAnimationOne.animation[frameToShow3][i]);
        }

        // Check if the animation has finished
        if (frameToShow3 == this.fallAnimationOne.animation.length - 1) {
          // Reset the game state and player positions
          this.gameState = "START";
          playerOne.position = 3;
          playerOne.level = 0;
          playerTwo.position = 0;
          playerTwo.level = 0;

          // Reset the fallAnimation to null so it can be recreated on the next "Death" state
          this.fallAnimationOne = null;
        }
        this.startTime = millis();
        break;
      case "DeathTwo":
        // display.fadeAway(playerOne.position);
        // for (let i = playerTwo.position; i < playerOne.position; i++) {
        //   display.fadeAway(i);
        // }
        // this.gameState = "START";
        // break;
        if (!this.fallAnimationTwo) {
          this.fallAnimationTwo = new FallTwo(playerOne, playerTwo, display);
        }

        let frameToShow4 = this.fallAnimationTwo.currentFrame(); // Get the current frame

        // Update the display buffer with the current frame of the animation
        for (let i = 0; i < this.fallAnimationTwo.pixels; i++) {
          display.setPixel(i, this.fallAnimationTwo.animation[frameToShow4][i]);
        }

        // Check if the animation has finished
        if (frameToShow4 == this.fallAnimationTwo.animation.length - 1) {
          // Reset the game state and player positions
          this.gameState = "START";
          playerOne.position = 3;
          playerOne.level = 0;
          playerTwo.position = 0;
          playerTwo.level = 0;

          // Reset the fallAnimation to null so it can be recreated on the next "Death" state
          this.fallAnimationTwo = null;
        }
        this.startTime = millis();

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

    let volume = map(distance, requiredDistance, halfDisplaySize, 1.0, 0.0);
    sound.setVolume(volume);

    if (distance < requiredDistance) {
      //console.log("Players are too close!");
      sound.stop();
      // Play animation for too close
      this.gameState = "CLOSE";
    } else if (distance > halfDisplaySize) {
      sound.stop();
      //console.log("Players are too far!");
      this.gameState = "FAR";
    }
  }

  checkVoid() {
    if (ground[playerOne.position] === "VOID" && !keyPressedFlag) {
      playerOne.voidTimer++; // Increment the timer if player one is on void space and no key is pressed
      //console.log("Player One on void space. Timer:", playerOne.voidTimer);
      if (playerOne.voidTimer >= 20) {
        // //console.log(
        //   "Player One has been on void space for more than 1 second."
        // );
        sound.stop();
        this.gameState = "DeathOne";
        // Add any additional actions you want to take when player loses
      }
    } else {
      playerOne.voidTimer = 0; // Reset the timer if player is not on void space or a key is pressed
      //console.log("Player One not on void space. Timer reset.");
    }

    if (ground[playerTwo.position] === "VOID" && !keyPressedFlag) {
      playerTwo.voidTimer++; // Increment the timer if player two is on void space and no key is pressed
      //console.log("Player Two on void space. Timer:", playerTwo.voidTimer);
      if (playerTwo.voidTimer >= 20) {
        // console.log(
        //   "Player Two has been on void space for more than 1 second."
        // );
        sound.stop();
        this.gameState = "DeathTwo";
        // Add any additional actions you want to take when player loses
      }
    } else {
      playerTwo.voidTimer = 0; // Reset the timer if player is not on void space or a key is pressed
      //console.log("Player Two not on void space. Timer reset.");
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

  if (sound.isLoaded()) {
    sound.play();
  }

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
