#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Global variables
int board[9] = {0};
int flag = 0;

// Function prototypes
void print_board();
int is_valid_move(int row, int col);
int has_winner(int player);
int is_board_full();
int evaluate_board();
int minimax(int depth, int is_maximizing);
void make_best_move();
void play_game();

// Function implementations

// Print the current state of the Tic-Tac-Toe board
void print_board()
{
  printf("-------------\n");
  for (int i = 0; i < 3; i++)
  {
    printf("| ");
    for (int j = 0; j < 3; j++)
    {
      if (board[3 * i + j] == 1)
      {
        printf("X | ");
      }
      else if (board[3 * i + j] == 2)
      {
        printf("O | ");
      }
      else
      {
        printf("  | ");
      }
    }
    printf("\n-------------\n");
  }
}

// Check if a move is valid
int is_valid_move(int row, int col)
{
  return row >= 0 && row < 3 && col >= 0 && col < 3 && board[3 * row + col] == 0;
}

// Check if a player has won
int has_winner(int player)
{
  for (int i = 0; i < 3; i++)
  {
    if (board[3 * i] == player && board[3 * i + 1] == player && board[3 * i + 2] == player)
    {
      return 1;
    }
    if (board[i] == player && board[i + 3] == player && board[i + 6] == player)
    {
      return 1;
    }
  }
  if (board[0] == player && board[4] == player && board[8] == player)
  {
    return 1;
  }
  if (board[2] == player && board[4] == player && board[6] == player)
  {
    return 1;
  }
  return 0;
}

// Check if the board is full
int is_board_full()
{
  for (int i = 0; i < 9; i++)
  {
    if (board[i] == 0)
    {
      return 0;
    }
  }
  return 1;
}

// Evaluate the current state of the board
int evaluate_board()
{
  if (has_winner(1))
  {
    return 10;
  }
  if (has_winner(2))
  {
    return -10;
  }
  return 0;
}

// Minimax algorithm for AI move calculation
int minimax(int depth, int is_maximizing)
{
  int score = evaluate_board();
  if (score != 0)
  {
    return score;
  }
  if (is_board_full())
  {
    return 0;
  }
  if (is_maximizing)
  {
    int best_score = -10000;
    for (int i = 0; i < 3; i++)
    {
      for (int j = 0; j < 3; j++)
      {
        if (board[3 * i + j] == 0)
        {
          board[3 * i + j] = 1;
          best_score = max(best_score, minimax(depth + 1, 0));
          board[3 * i + j] = 0;
        }
      }
    }
    return best_score;
  }
  else
  {
    int best_score = 10000;
    for (int i = 0; i < 3; i++)
    {
      for (int j = 0; j < 3; j++)
      {
        if (board[3 * i + j] == 0)
        {
          board[3 * i + j] = 2;
          best_score = min(best_score, minimax(depth + 1, 1));
          board[3 * i + j] = 0;
        }
      }
    }
    return best_score;
  }
}

// Make the best move for AI
void make_best_move()
{
  int best_score = -10000;
  int best_move_row = -1;
  int best_move_col = -1;
  for (int i = 0; i < 3; i++)
  {
    for (int j = 0; j < 3; j++)
    {
      if (board[3 * i + j] == 0)
      {
        board[3 * i + j] = 1;
        int move_score = minimax(0, 0);
        if (move_score > best_score)
        {
          best_score = move_score;
          best_move_row = i;
          best_move_col = j;
        }
        board[3 * i + j] = 0;
      }
    }
  }
  if (best_move_row != -1 && best_move_col != -1)
  {
    board[3 * best_move_row + best_move_col] = 1;
  }
}

// Main function to play the game
void play_game()
{
  for (int i = 0; i < 9; i++)
  {
    board[i] = 0;
  }
  make_best_move();
  while (!has_winner(1) && !has_winner(2) && !is_board_full())
  {
    print_board();
    int row, col;
    printf("Enter your move (row, column, 0 indexing): ");
    scanf("%d %d", &row, &col);
    if (is_valid_move(row, col))
    {
      board[3 * row + col] = 2;
      if (has_winner(2))
      {
        print_board();
        printf("You win!\n");
        flag = 1;
        printf("It can't be...\n");
        printf("BITSCTF{n0t_th4T_eZ}\n");
      }
      else if (is_board_full())
      {
        print_board();
        printf("It's a draw!\n");
        return;
      }
      make_best_move();
      if (has_winner(1))
      {
        print_board();
        printf("AI wins (not really)!\n");
        return;
      }
      if (is_board_full())
      {
        print_board();
        printf("It's a draw!\n");
        return;
      }
    }
    else
    {
      printf("Invalid move! Try again.\n");
    }
  }
}

int main()
{
  play_game();
  return 0;
}
