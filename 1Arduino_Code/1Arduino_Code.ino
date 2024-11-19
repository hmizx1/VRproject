int LED1 = 13;  // Pin number for AI's first LED
int LED2 = 12;  // Pin number for AI's second LED
int LED3 = 11;  // Pin number for AI's third LED
int LED4 = 7;   // Pin number for player's first LED
int LED5 = 6;   // Pin number for player's second LED
int LED6 = 5;   // Pin number for player's third LED
int buzzer = 15; // Pin number for buzzer
int button = 14; // Pin number for game start button

int playerScore = 0; // Player's score
int aiScore = 0; // AI's score

void setup() {
  // Set pin modes for LEDs, buzzer, and button
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(LED5, OUTPUT);
  pinMode(LED6, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(button, INPUT_PULLUP);

  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
}

void loop() {
  // Button press detection
  if (digitalRead(button) == LOW) {
    delay(50); // Delay for debouncing
    if (digitalRead(button) == LOW) {
      Serial.println('S'); // Send signal to start game
      while (digitalRead(button) == LOW); // Wait until button release
    }
  }

  // Read data from serial if available
  if (Serial.available() > 0) {
    char result = Serial.read(); // Read the result

    // Update scores and LEDs based on the game result
    if (result == 'P') { // Player wins
      if (playerScore == 0) digitalWrite(LED4, HIGH);
      else if (playerScore == 1) digitalWrite(LED5, HIGH);
      else if (playerScore == 2) digitalWrite(LED6, HIGH);
      playerScore++;
    } else if (result == 'A') { // AI wins
      if (aiScore == 0) digitalWrite(LED1, HIGH);
      else if (aiScore == 1) digitalWrite(LED2, HIGH);
      else if (aiScore == 2) digitalWrite(LED3, HIGH);
      aiScore++;
    }

    // Check if there's a winner
    if (playerScore == 3 || aiScore == 3) {
      playWinningBuzzer(); // Play winning sound
      resetGame((playerScore == 3) ? LED4 : LED1, (playerScore == 3) ? LED5 : LED2, (playerScore == 3) ? LED6 : LED3, (playerScore == 3) ? playerScore : aiScore);
    }
  }
}

void playWinningBuzzer() {
  // Sound buzzer in intervals
  for (int i = 0; i < 3; i++) {
    digitalWrite(buzzer, HIGH);
    delay(200);
    digitalWrite(buzzer, LOW);
    delay(200);
  }
}

void resetGame(int led1, int led2, int led3, int &score) {
  // Flash LEDs and reset score
  for (int i = 0; i < 5; i++) {
    digitalWrite(led1, LOW);
    digitalWrite(led2, LOW);
    digitalWrite(led3, LOW);
    delay(500);
    digitalWrite(led1, HIGH);
    digitalWrite(led2, HIGH);
    digitalWrite(led3, HIGH);
    delay(500);
  }
  score = 0;
}
