class winAnimation {
  constructor(playerOne, playerTwo, display) {
    this.numberOfFrames = 100; // how many frames the animation has
    this.start = playerTwo.position;
    this.end = playerOne.position;
    this.displayBuffer = display.displayBuffer;
    this.animation = new Array(this.numberOfFrames);
    this.pixels = this.displayBuffer.length;
    this.currentFrameCount = -1;

    // Calculate the midpoint for the transition
    //const midpoint = Math.floor(this.pixels / 2);
    let k = 0;
    for (let i = 0; i < this.numberOfFrames; i++) {
      const midpoint = this.pixels;
      this.animation[i] = new Array(this.pixels);

      for (let j = 0; j < this.pixels; j++) {
        let t;
        if (j < midpoint) {
          t = j / midpoint; // Normalize j to a value between 0 and 1 for the first half
        } else {
          t = 1 - (j - midpoint) / midpoint; // Normalize j to a value between 1 and 0 for the second half
        }

        let blendedColor;
        if (i < this.numberOfFrames / 2) {
          // First half of the animation, transition from playerOne to playerTwo
          blendedColor = lerpColor(
            playerOne.playerColor,
            playerTwo.playerColor,
            t
          );
        } else {
          // Second half of the animation, transition from playerTwo to playerOne
          blendedColor = lerpColor(
            playerTwo.playerColor,
            playerOne.playerColor,
            t
          );
        }
        this.animation[i][j] = blendedColor;
        k += 0.01;
      }
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
