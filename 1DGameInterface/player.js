// This holds some player information, like color and position.
// It also has some player methods for managing how a player moves.

class Player {
  constructor(_color, _position, _displaySize) {
    this.playerColor = _color;
    this.position = _position;
    this.score = 0;
    this.displaySize = _displaySize;
    this.level = 0; // Initialize the level to 0
    this.isDashing = false; // Initialize dashing flag
  }

  // Move player based on keyboard input
  move(_direction) {
    // increments or decrements player position
    this.position = this.position + _direction;

    // if player hits the edge of display, loop around
    if (this.position < 0) {
      //==-1
      this.position = this.displaySize - 1;
    } else if (this.position >= this.displaySize) {
      this.position -= this.displaySize;
      this.level++;
    }
  }
  moveWhileDashing(_direction) {
    if (this.isDashing) {
      this.move(_direction);
      setTimeout(() => this.moveWhileDashing(_direction), 100); // Call moveWhileDashing again after 1 second
    }
  }
  startDash(_direction) {
    this.isDashing = true;
    this.moveWhileDashing(1); // Start moving immediately
  }

  stopDash() {
    this.isDashing = false;
  }
}
