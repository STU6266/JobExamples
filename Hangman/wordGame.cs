using System;
using System.IO;  // Include this namespace to enable file reading

namespace WordGuessingGame
{
    class Program
    {
        static void Main(string[] args)
        {
            // Define the path to the words file. 
            // The file should contain a list of words (one word per line).
            string filePath = "words.txt";
            string[] words;

            // Attempt to read all lines from the file into the 'words' array.
            try
            {
                words = File.ReadAllLines(filePath);
            }
            catch (Exception e)
            {
                Console.WriteLine("Error: Could not read the words file.");
                Console.WriteLine($"Exception: {e.Message}");
                return;  // Exit if the word list cannot be loaded
            }

            // If the file is empty, we cannot play the game.
            if (words.Length == 0)
            {
                Console.WriteLine("The words file is empty. Please add some words to play the game.");
                return;
            }

            // Ask the player to choose a difficulty level.
            Console.Write("Choose difficulty (easy, medium, hard): ");
            string? difficultyInput = Console.ReadLine();
            if (difficultyInput == null) difficultyInput = "";  // Handle null just in case
            string difficulty = difficultyInput.Trim().ToLower();

            // Determine word length range based on chosen difficulty.
            int minLength, maxLength;
            switch (difficulty)
            {
                case "easy":
                    // Easy: shorter words (for example, 1 to 5 letters)
                    minLength = 1;
                    maxLength = 5;
                    break;
                case "medium":
                    // Medium: medium-length words (for example, 6 to 8 letters)
                    minLength = 6;
                    maxLength = 8;
                    break;
                case "hard":
                    // Hard: longer words (for example, 9 or more letters)
                    minLength = 9;
                    maxLength = int.MaxValue;
                    break;
                default:
                    // If an invalid difficulty was entered, default to easy.
                    Console.WriteLine("Invalid difficulty choice. Defaulting to EASY.");
                    minLength = 1;
                    maxLength = 5;
                    break;
            }

            // Filter the list of words to those matching the difficulty length range.
            string[] filteredWords = Array.FindAll(words, w =>
            {
                int len = w.Trim().Length;
                return len >= minLength && len <= maxLength;
            });

            // If no words match the difficulty criteria, use all words as a fallback.
            if (filteredWords.Length == 0)
            {
                Console.WriteLine("No words found for the selected difficulty. Using all available words.");
                filteredWords = words;
            }

            // Select a random word from the filtered list.
            Random random = new Random();
            string secretWord = filteredWords[random.Next(filteredWords.Length)].Trim();
            // Convert the secret word to lowercase for consistent comparison (game will be case-insensitive).
            secretWord = secretWord.ToLower();

            // Prepare the game state
            char[] revealedWord = new char[secretWord.Length];  // Array for revealed letters and underscores
            for (int i = 0; i < revealedWord.Length; i++)
            {
                revealedWord[i] = '_';  // start with all letters hidden
            }
            int wrongGuesses = 0;                  // count of wrong letters guessed
            const int maxWrongGuesses = 10;        // maximum wrong guesses allowed (11th wrong guess means game over)
            var guessedLetters = new List<char>(); // list to track all letters that have been guessed

            // Greet the player and display initial game info
            Console.WriteLine("\nWelcome to Hangman!");
            Console.WriteLine($"I have chosen a word that has {secretWord.Length} letters.");
            Console.WriteLine($"You have {maxWrongGuesses} wrong attempts allowed. Let's begin!");
            Console.WriteLine();  // blank line for spacing

            // Game loop: continue until the word is guessed or player runs out of attempts
            while (wrongGuesses < maxWrongGuesses && new string(revealedWord) != secretWord)
            {
                // Display the current state of the word (with underscores for missing letters)
                Console.Write("Word: ");
                foreach (char c in revealedWord)
                {
                    Console.Write(c + " ");
                }
                Console.WriteLine();  // end of word display line

                // Prompt the player for a letter guess
                Console.Write("Guess a letter: ");
                string? input = Console.ReadLine();
                if (input == null)
                {
                    // If no input (null), continue to next iteration (or break, as we cannot continue without input)
                    Console.WriteLine("Input cannot be null. Please try again.");
                    continue;
                }
                input = input.Trim().ToLower();
                if (input.Length == 0)
                {
                    // If the user entered an empty string (just pressed Enter)
                    Console.WriteLine("You did not enter a letter. Please try again.");
                    continue;
                }
                if (input.Length > 1)
                {
                    // If the user entered more than one character, ask for a single letter.
                    Console.WriteLine("Please enter only a single letter.");
                    continue;
                }

                char guess = input[0];
                // Check if the character is alphabetic (a-z). If not, ignore it.
                if (!char.IsLetter(guess))
                {
                    Console.WriteLine("Invalid input. Please enter a letter (a-z).");
                    continue;
                }

                // Check if this letter was already guessed before
                if (guessedLetters.Contains(guess))
                {
                    Console.WriteLine($"You already guessed '{guess}'. Try a different letter.");
                    continue;
                }

                // Add the guessed letter to the list of attempted letters
                guessedLetters.Add(guess);

                // Check if the guessed letter is in the secret word
                if (secretWord.Contains(guess))
                {
                    // Correct guess: reveal all occurrences of this letter in the word
                    for (int i = 0; i < secretWord.Length; i++)
                    {
                        if (secretWord[i] == guess)
                        {
                            revealedWord[i] = guess;  // reveal the letter at position i
                        }
                    }
                    Console.WriteLine($"Good job! The letter '{guess}' is in the word.");
                }
                else
                {
                    // Wrong guess: increment the wrong guess counter
                    wrongGuesses++;
                    Console.WriteLine($"Sorry, the letter '{guess}' is not in the word.");
                    int attemptsLeft = maxWrongGuesses - wrongGuesses;
                    if (attemptsLeft > 0)
                    {
                        Console.WriteLine($"Wrong attempts: {wrongGuesses}. You have {attemptsLeft} more wrong attempts left.");
                    }
                }

                // Draw the current Hangman figure (show progress of the gallows and figure)
                PrintHangmanFigure(wrongGuesses);
                Console.WriteLine();  // blank line for spacing between turns

            } // end of game loop

            // After exiting the loop, check the reason (win or lose)
            if (new string(revealedWord) == secretWord)
            {
                // The loop ended because the word was guessed correctly
                Console.WriteLine("\nCongratulations! You guessed the word!");
            }
            else if (wrongGuesses >= maxWrongGuesses)
            {
                // The loop ended because the player ran out of attempts (loss condition)
                Console.WriteLine("\nGame Over! You've used all your attempts.");
                Console.WriteLine($"The word was: {secretWord}");
                // Optionally, draw the final state of the hangman (fully hung) one last time
                PrintHangmanFigure(maxWrongGuesses);
            }
        }

        // This method prints the hangman scaffold and figure according to the number of wrong guesses.
        static void PrintHangmanFigure(int wrongGuesses)
        {
            // We will build the hangman figure step by step.
            // There are 12 possible wrong guesses, and each will add a new part to the gallows or the figure.
            // Stage 0 (wrongGuesses = 0): nothing is drawn yet.
            // Stage 1: Draw the base platform.
            // Stage 2: Draw the vertical support pole.
            // Stage 3: Draw the top crossbeam.
            // Stage 4: Draw the rope hanging down from the crossbeam.
            // Stage 5: Draw the head of the hangman.
            // Stage 6: Draw the torso (body) of the hangman.
            // Stage 7: Draw the left arm.
            // Stage 8: Draw the right arm.
            // Stage 9: Draw the left leg.
            // Stage 10: Draw the right leg (complete figure at this point).

            // Use a switch or if-else to draw according to stage.
            // For simplicity, we'll handle each stage explicitly.
            switch (wrongGuesses)
            {
                default:
                case 0:
                    // No wrong guesses: draw nothing (no gallows, no figure yet).
                    break;
                case 1:
                    // 1 wrong guess: Draw the base of the gallows.
                    Console.WriteLine("      ");
                    Console.WriteLine("      ");
                    Console.WriteLine("      ");
                    Console.WriteLine("      ");
                    Console.WriteLine("      ");
                    Console.WriteLine("=======");  // base platform on the ground
                    break;
                case 2:
                    // 2 wrong guesses: Draw the upright support pole (on left side) on top of the base.
                    Console.WriteLine(" |    ");
                    Console.WriteLine(" |    ");
                    Console.WriteLine(" |    ");
                    Console.WriteLine(" |    ");
                    Console.WriteLine(" |    ");
                    Console.WriteLine("=======");  // base remains
                    break;
                case 3:
                    // 3 wrong guesses: Draw the top crossbeam on the pole.
                    Console.WriteLine(" +---+");
                    Console.WriteLine(" |   |");
                    Console.WriteLine(" |    ");
                    Console.WriteLine(" |    ");
                    Console.WriteLine(" |    ");
                    Console.WriteLine("=======");  // base
                    break;
                case 4:
                    // 4 wrong guesses: Draw the rope hanging from the crossbeam.
                    Console.WriteLine(" +---+");
                    Console.WriteLine(" |   |");
                    Console.WriteLine(" |   |");   // rope (vertical line from the crossbeam)
                    Console.WriteLine(" |    ");
                    Console.WriteLine(" |    ");
                    Console.WriteLine("=======");
                    break;
                case 5:
                    // 5 wrong guesses: Draw the head of the figure.
                    Console.WriteLine(" +---+");
                    Console.WriteLine(" |   |");
                    Console.WriteLine(" |   O");   // head of the hangman
                    Console.WriteLine(" |   |");   // partial torso (just to connect head)
                    Console.WriteLine(" |    ");
                    Console.WriteLine("=======");
                    break;
                case 6:
                    // 6 wrong guesses: Draw the torso (body) of the figure.
                    Console.WriteLine(" +---+");
                    Console.WriteLine(" |   |");
                    Console.WriteLine(" |   O");
                    Console.WriteLine(" |   |");   // full torso
                    Console.WriteLine(" |   |");   // torso extends a bit (optional, drawing torso on two lines for clarity)
                    Console.WriteLine("=======");
                    break;
                case 7:
                    // 7 wrong guesses: Draw the left arm.
                    Console.WriteLine(" +---+");
                    Console.WriteLine(" |   |");
                    Console.WriteLine(" |   O");
                    Console.WriteLine(" |  /|");   // left arm added (slash before torso)
                    Console.WriteLine(" |   |");   // torso
                    Console.WriteLine("=======");
                    break;
                case 8:
                    // 8 wrong guesses: Draw the right arm.
                    Console.WriteLine(" +---+");
                    Console.WriteLine(" |   |");
                    Console.WriteLine(" |   O");
                    Console.WriteLine(" |  /|\\");  // both arms added (slash and backslash for arms)
                    Console.WriteLine(" |   |");    // torso
                    Console.WriteLine("=======");
                    break;
                case 9:
                    // 9 wrong guesses: Draw the left leg.
                    Console.WriteLine(" +---+");
                    Console.WriteLine(" |   |");
                    Console.WriteLine(" |   O");
                    Console.WriteLine(" |  /|\\");  // arms
                    Console.WriteLine(" |  / ");    // left leg added
                    Console.WriteLine("=======");
                    break;
                case 10:
                    // 10 wrong guesses: Draw the right leg (figure is now complete).
                    Console.WriteLine(" +---+");
                    Console.WriteLine(" |   |");
                    Console.WriteLine(" |   O");
                    Console.WriteLine(" |  /|\\");
                    Console.WriteLine(" |  / \\");   // both legs added
                    Console.WriteLine("=======");
                    break;

            }
        }
    }
}
