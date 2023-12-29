#include <dirent.h>
#include <fcntl.h>
#include <linux/input-event-codes.h>
#include <linux/input.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
// gcc keystroke.c -o key && sudo ./key

#define MAX_FILES 100 // Maximum number of files to handle

// Replace with the appropriate key codes (tested with svlatin1)
#define BACKSPACE_KEY 14
#define DELETE_KEY 111
#define SPACE_KEY 57
#define ENTER_KEY 28

#define SECONDS_PER_HOUR 5 // Number of seconds in an hour
#define INTERVAL 10
#define TO_MINUTE 60.0 / INTERVAL
#define INFLATION 0.9

#define AVG_WORD_LENGTH 5

#define THRESHOLD 2
char path[100];
volatile sig_atomic_t flag = 0;

void sigint_handler(int sig) { flag = 1; }

#define MAX_FILES 100

void findFiles(const char *directoryPath, const char *pattern, char *files[],
               int *fileCount) {
  DIR *directory = opendir(directoryPath);
  if (directory != NULL) {
    struct dirent *entry;
    while ((entry = readdir(directory)) != NULL) {
      if (strstr(entry->d_name, pattern) != NULL) {
        int combinedLength = strlen(directoryPath) + strlen(entry->d_name) + 1;
        files[*fileCount] = (char *)malloc(combinedLength * sizeof(char));
        if (files[*fileCount] != NULL) {
          strcpy(files[*fileCount], directoryPath);
          strcat(files[*fileCount], entry->d_name);

          printf("%d. %s\n", *fileCount + 1, entry->d_name);
          (*fileCount)++;
        }
      }
    }
    closedir(directory);
  }
}

void getKBDFile() {
  const char *paths[] = {"/dev/input/by-id/", "/dev/input/by-path/"};
  const char *pattern = "-kbd";
  char *files[MAX_FILES];
  int fileCount = 0;

  for (int i = 0; i < sizeof(paths) / sizeof(paths[0]); ++i) {
    findFiles(paths[i], pattern, files, &fileCount);
  }

  if (fileCount == 0) {
    goto exit_;
  }

  // Ask user to select a file by number
  int chosenFileNum;
  printf("Enter the number corresponding to your keyboard: ");
  scanf("%d", &chosenFileNum);

  // Validate the input number
  if (chosenFileNum < 1 || chosenFileNum > fileCount) {
    goto exit_;
  }

  // Use the chosen file
  printf("\nYou chose: %s\n", files[chosenFileNum - 1]);
  printf("-------------------------------------\n\n");
  strcpy(path, files[chosenFileNum - 1]);

exit_:
  // Free memory allocated for file names
  for (int i = 0; i < fileCount; i++) {
    free(files[i]);
  }

  if (fileCount == 0) {
    perror("No keyboards detected!\n");
    exit(EXIT_FAILURE);
  } else if (chosenFileNum < 1 || chosenFileNum > fileCount) {
    perror("Invalid selection\n");
    exit(EXIT_FAILURE);
  }
}

// SvLatin1
int isCharacter(int c) {
  return ((0x20 < c) && (c < 0x7F)) || (0xA0 < c) && (c != 0xAD);
}

double estimateFrequency(double previousFrequency, double deltaCount,
                         time_t timeInterval, double smoothingFactor) {
  double instantaneousFrequency = deltaCount / timeInterval;
  return (smoothingFactor * instantaneousFrequency) +
         ((1 - smoothingFactor) * previousFrequency);
}

void loop() {
  int fd;
  struct input_event ev;
  int errorCount = 0;
  int wordCount = 0;
  int characterCount = 0;
  time_t previous_time = time(NULL) - SECONDS_PER_HOUR + 1;

  fd = open(path,
            O_RDONLY | O_NONBLOCK); // Replace X with the appropriate event
                                    // number for the keyboard

  if (fd == -1) {
    perror("Cannot open input device");
    printf("\nAre your root?\n");
    return;
  }

  printf("Refresh rate: %ds\n\n", INTERVAL);

  printf("\rPress any key to continue");
  fflush(stdout);

  double wps = 0.0;
  double error = 0.0;

  int i = 0;

  double wpm = 0.0;
  double accuracy = 0.0;

  char *modes[3] = {"Inactive", "Working", "Typing"};
  int mode = 0;
  while (!flag) {
    if (access(path, F_OK) == -1) {
      printf("Keyboard does not exist anymore. Exiting.\n");
      break;
    }

    fd_set set;
    FD_ZERO(&set);
    FD_SET(fd, &set);

    struct timeval timeout;
    timeout.tv_sec = INTERVAL * 2;
    timeout.tv_usec = 0;

    // Use select() to wait for data with timeout
    int ready = select(fd + 1, &set, NULL, NULL, &timeout);

    if (ready == -1) {
      perror("Error in select");
      break;
    } else if (ready == 0) {
      mode = 0;
      goto skip;

    } else {
      ssize_t status = read(fd, &ev, sizeof(struct input_event));

      if (status == -1) {
        break;
      }
    }

    if (ev.type == EV_KEY && (ev.value == 1 || ev.value == 0)) {
      switch (ev.code) {
      case BACKSPACE_KEY:
      case DELETE_KEY:
        errorCount++;
        break;
      case ENTER_KEY:
      case SPACE_KEY:
        wordCount++;
        break;
      default:
        if (isCharacter(ev.code)) {
          characterCount++; // This code is dangerous since ev.code contains
                            // typed character (keylogger)
        }

        break;
      }

      i++;
      time_t current_time = time(NULL);
      double elapsed_seconds = difftime(current_time, previous_time);
      if (elapsed_seconds >= INTERVAL) {

        if (elapsed_seconds >= INTERVAL * 2) {
          mode = 0;
          goto skip;
        }

        if ((double)i / elapsed_seconds < 0.5) {
          mode = 1;
          goto skip;
        }

        mode = 2;
        double wc_prime = ((double)wordCount +
                           ((double)characterCount / (double)AVG_WORD_LENGTH)) /
                          2;
        wps = estimateFrequency(wps, wc_prime, elapsed_seconds, 0.5);

        error =
            estimateFrequency(error, 100.0 * errorCount / (double)i, 1.0, 0.3);

        wpm = wps * 60.0 * (1.0 - error / 100.0) * INFLATION;
        accuracy = 100.0 - error;

      skip:
        errorCount = 0;
        wordCount = 0;
        characterCount = 0;
        previous_time = current_time;
        i = 0;
      print:

        printf("\r Rate: %.2fWPM Accuracy: %.1f%%  (%s)   "
               "        ",
               wpm, accuracy, modes[mode]);
        fflush(stdout);
      } else {
        if (mode != 2) {
          mode = 2;
          goto print;
        }
      }
    }
  }
  printf("Closing\n\n");
  printf("Thank you for using typingstat!\n");
  close(fd);
}

const char *eula =
    "\n                         [EULA]\n\n"
    "This software contains a keylogger and is for educational purposes only.\n"
    "It counts keystrokes and does not store characters directly. By using \n"
    "this software, you agree that the developer takes ZERO legal \n"
    "responsibility for its use. It is your responsibility to use this \n"
    "software ethically and in compliance with applicable laws. Be aware of \n"
    "potential hazards and obtain necessary permissions before monitoring \n"
    "keystrokes. Have fun!\n\n";

int main() {
  signal(SIGINT, sigint_handler); // Set up SIGINT signal handler

  printf("%s", eula);
  char input[50]; // Assuming input won't exceed 49 characters

  printf("Type 'logger' to proceed: ");
  fgets(input, sizeof(input), stdin);

  // Remove newline character if present
  input[strcspn(input, "\n")] = '\0';

  // Compare the user input with the desired string
  if (strcmp(input, "logger") != 0) {
    perror("You must accept the notice.\n");
    exit(EXIT_FAILURE);
  }
  printf("\n\nList of available keyboards:\n");
  getKBDFile();

  loop();

  return 0;
}
