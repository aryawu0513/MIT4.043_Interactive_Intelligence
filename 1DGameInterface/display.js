// This is used to aggregrate visual information from all objects before we display them.
// First we populate display and then we show it to user.
// This is particularly helpful once you start outputting your game to an LED strip, of if you want to have two separate 'screens'

class Display {
  constructor(_displaySize, _pixelSize, ground) {
    this.displaySize = _displaySize;
    this.pixelSize = _pixelSize;
    this.initColor = color(0, 0, 0); // black color
    this.displayBuffer = [];
    this.ground = ground;
  }

  // Color a specific pixel in the buffer
  setPixel(_index, _color) {
    this.displayBuffer[_index] = _color;
  }

  // Color all pixels in the buffer
  setAllPixels(_color) {
    for (let i = 0; i < displaySize; i++) {
      display.setPixel(i, _color);
    }
  }

  setGround(ground) {
    for (let i = 0; i < this.displaySize; i++) {
      // console.log("before", this.displayBuffer[i]);
      this.displayBuffer[i] = ground[i] === "GROUND" ? color(255) : color(0);
      // console.log("ground", this.displayBuffer[i]);
    }
  }
  setGradientColors(
    playerOnePosition,
    playerTwoPosition,
    playerOneColor,
    playerTwoColor
  ) {
    let start = min(playerOnePosition, playerTwoPosition);
    let end = max(playerOnePosition, playerTwoPosition);

    for (let i = start + 1; i < end; i++) {
      let distanceToPlayerOne = abs(i - playerOnePosition);
      let distanceToPlayerTwo = abs(i - playerTwoPosition);
      let totalDistance = distanceToPlayerOne + distanceToPlayerTwo;

      let redAmount =
        (distanceToPlayerTwo / totalDistance) * red(playerOneColor) +
        (distanceToPlayerOne / totalDistance) * red(playerTwoColor);
      let blueAmount =
        (distanceToPlayerTwo / totalDistance) * blue(playerOneColor) +
        (distanceToPlayerOne / totalDistance) * blue(playerTwoColor);

      let gradientColor = color(redAmount, 0, blueAmount);
      console.log("gradientColor", gradientColor);
      this.displayBuffer[i] = lerpColor(
        this.displayBuffer[i],
        gradientColor,
        0.5
      ); // Use lerpColor for smooth transitions
      console.log("displayBuffer", this.displayBuffer[i]);
    }
  }

  // Now write it to screen
  show() {
    for (let i = 0; i < this.displaySize; i++) {
      fill(this.displayBuffer[i]);
      rect(
        i * this.pixelSize,
        2 * this.pixelSize,
        this.pixelSize,
        this.pixelSize
      );
    }
    // if (controller.gameState === "WIN") {
    //   let totalTime = controller.totalTime;
    //   fill(255);
    //   textSize(16);
    //   text("Time: " + totalTime.toFixed(2) + "s", 10, 20);
    // } else {
    //   let totalTime = (millis() - controller.startTime) / 1000;
    //   console.log("HERE", totalTime);
    //   fill(255);
    //   textSize(16);
    //   text("Time: " + totalTime.toFixed(2) + "s", 10, 20);
    // }
  }

  // Let's empty the display before we start adding things to it again
  clear() {
    for (let i = 0; i < this.displaySize; i++) {
      this.displayBuffer[i] = this.initColor;
    }
  }
}
