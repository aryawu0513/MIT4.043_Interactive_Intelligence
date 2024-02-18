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

  // Now write it to screen
  // This is the only function in the entire software that writes something directly to the screen. I recommend you keep it this way.
  // show() {
  //   for (let i = 0; i < this.displaySize; i++) {
  //     fill(this.displayBuffer[i]);
  //     rect(i * this.pixelSize, 0, this.pixelSize, this.pixelSize, 1);
  //   }
  //   if (controller.gameState === "PLAY") {
  //     let totalTime = (millis() - controller.startTime) / 1000;
  //     fill(255);
  //     textSize(16);
  //     text("Time: " + totalTime.toFixed(2) + "s", 10, 20);
  //   }
  // }
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
    if (controller.gameState === "WIN") {
      let totalTime = controller.totalTime;
      fill(255);
      textSize(16);
      text("Time: " + totalTime.toFixed(2) + "s", 10, 20);
    } else {
      let totalTime = (millis() - controller.startTime) / 1000;
      console.log("HERE", totalTime);
      fill(255);
      textSize(16);
      text("Time: " + totalTime.toFixed(2) + "s", 10, 20);
    }
  }

  // Let's empty the display before we start adding things to it again
  clear() {
    for (let i = 0; i < this.displaySize; i++) {
      this.displayBuffer[i] = this.initColor;
    }
  }
}
