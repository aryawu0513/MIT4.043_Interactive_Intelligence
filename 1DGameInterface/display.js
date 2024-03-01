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
    let start = playerTwoPosition;
    let end = playerOnePosition;
    if (start <= end) {
      for (let i = start + 1; i < end; i++) {
        let distance = abs(playerOnePosition - playerTwoPosition);
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
        // Calculate the midpoint
        // Calculate lerpFactor based on distance
        let lerpFactor;
        if (distance <= 5) {
          lerpFactor = map(distance, 3 - playerTwo.level, 5, 0.1, 0.7);
        } else if (distance >= 10) {
          lerpFactor = map(distance, 10, 15, 0.7, 0.1);
        } else {
          lerpFactor = 0.7;
        }
        //let lerpFactor = map(distance, 2, 15, 0.7, 0.3); // Adjust lerp factor based on distance
        this.displayBuffer[i] = lerpColor(
          this.displayBuffer[i],
          gradientColor,
          lerpFactor
        ); // Use lerpColor for smooth transitions
      }
    } else {
      for (let i = start + 1; i < this.displaySize; i++) {
        let distanceToPlayerOne = abs(playerOnePosition + this.displaySize - i);
        let distanceToPlayerTwo = abs(i - playerTwoPosition);
        let totalDistance = distanceToPlayerOne + distanceToPlayerTwo;
        let redAmount =
          (distanceToPlayerTwo / totalDistance) * red(playerOneColor) +
          (distanceToPlayerOne / totalDistance) * red(playerTwoColor);
        let blueAmount =
          (distanceToPlayerTwo / totalDistance) * blue(playerOneColor) +
          (distanceToPlayerOne / totalDistance) * blue(playerTwoColor);

        let gradientColor = color(redAmount, 0, blueAmount);
        this.displayBuffer[i] = lerpColor(
          this.displayBuffer[i],
          gradientColor,
          0.5
        ); // Use lerpColor for smooth transitions
      }
      for (let i = 0; i < end; i++) {
        let distanceToPlayerOne = abs(playerOnePosition);
        let distanceToPlayerTwo = abs(this.displaySize - playerTwoPosition + i);
        let totalDistance = distanceToPlayerOne + distanceToPlayerTwo;
        let redAmount =
          (distanceToPlayerTwo / totalDistance) * red(playerOneColor) +
          (distanceToPlayerOne / totalDistance) * red(playerTwoColor);
        let blueAmount =
          (distanceToPlayerTwo / totalDistance) * blue(playerOneColor) +
          (distanceToPlayerOne / totalDistance) * blue(playerTwoColor);

        let gradientColor = color(redAmount, 0, blueAmount);
        this.displayBuffer[i] = lerpColor(
          this.displayBuffer[i],
          gradientColor,
          0.5
        ); // Use lerpColor for smooth transitions
      }
    }
  }

  // fadeAway(position) {
  //   let pixelColor = this.displayBuffer[position];
  //   let backgroundColor =
  //     this.ground[position] === "GROUND" ? color(255) : color(0);
  //   for (let i = 0; i <= 100; i++) {
  //     let blendColor = lerpColor(pixelColor, backgroundColor, i / 100);
  //     setTimeout(() => {
  //       this.displayBuffer[position] = blendColor;
  //     }, i * 10); // Change the pixel color gradually over 1 second (1000 ms)
  //   }
  // }

  // Now write it to screen
  show() {
    let totalTime = (millis() - controller.startTime) / 1000;
    let alpha = map(totalTime, 0, 1000, 255, 0);
    alpha = constrain(alpha, 0, 255); // Ensure alpha is within valid range

    for (let i = 0; i < this.displaySize; i++) {
      let fadedColor = color(
        red(this.displayBuffer[i]),
        green(this.displayBuffer[i]),
        blue(this.displayBuffer[i]),
        alpha
      );
      fill(fadedColor);
      rect(
        i * this.pixelSize,
        2 * this.pixelSize,
        this.pixelSize,
        this.pixelSize
      );
    }
    if (controller.gameState === "WIN") {
      let totalTime = controller.totalTime;
      fill(255);
      textSize(16);
      text("Time: " + totalTime.toFixed(2) + "s", 10, 20);
    } else {
      let totalTime = (millis() - controller.startTime) / 1000;
      //console.log("HERE", totalTime);
      fill(255);
      textSize(16);
      //text("Time: " + totalTime.toFixed(2) + "s", 10, 20);
    }
    if (controller.gameState === "PLAY") {
      fill(255);
      textSize(16);
      //text("Distance: " + (3 - int(playerTwo.level)), 150, 20);
    }
  }

  // Let's empty the display before we start adding things to it again
  clear() {
    for (let i = 0; i < this.displaySize; i++) {
      this.displayBuffer[i] = this.initColor;
    }
  }
}
