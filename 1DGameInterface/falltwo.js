class FallTwo {
  constructor(playerOne, playerTwo, display) {
    this.numberOfFrames = 100; // how many frames the animation has
    this.start = playerTwo.position;
    this.end = playerOne.position;
    this.displayBuffer = display.displayBuffer;
    // Multidimensional arrays in javascript are a bit silly
    // I recommend you watch this to understand what is happening next: https://www.youtube.com/watch?v=OTNpiLUSiB4
    this.animation = new Array(this.numberOfFrames);
    this.pixels = this.displayBuffer.length;

    this.currentFrameCount = -1; // this tracks what frame we are currently reading

    // The animation mimics an explosion and this variable tracks where the wave is in the display
    let k = this.start;
    let tail = this.end;

    // Build up the array in this for loop
    for (let i = 0; i < this.numberOfFrames; i++) {
      // since javascript can't initialize a 2D array, we need to do this
      this.animation[i] = new Array(this.pixels);
      //animation is a 2D array

      // populate array with empty/black pixels
      for (let j = 0; j < this.pixels; j++) {
        this.animation[i][j] = this.displayBuffer[j];
      }
      this.displayBuffer[this.start] = color(0);

      // Then populate array with animation

      // Start from the center

      // Animate to the right
      //this.animation[i][k] = color(255, 255, 0);
      if (k < this.end) {
        this.displayBuffer[k] = this.displayBuffer[k + 1];
        //this.animation[i][k] = color(0, 0, 0);
      } else {
        this.displayBuffer[k] = color(255, 255, 255);
        k = this.start;
      }

      // Animate to the left
      // this.animation[i][center - k] = color(255, 255, 0);

      // Increment animation pixel
      k = k + 1;
    }
  }

  // This function advances animation to next frame and returns current frame number
  currentFrame() {
    this.currentFrameCount = this.currentFrameCount + 1;

    if (this.currentFrameCount >= this.numberOfFrames) {
      this.currentFrameCount = 0;
    }

    return this.currentFrameCount;
  }

  // Returns one pixel at a time
  grabPixel(_index) {
    return this.animation[this.currentFrameCount][_index];
  }
}
