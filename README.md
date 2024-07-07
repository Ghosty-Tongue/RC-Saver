# RC-Saver

RC-Saver is a Python script designed to interact with the Roblox Chat API, allowing users to fetch conversation IDs, archive messages, and save them into HTML or TXT files. This tool is useful for managing and storing Roblox chat histories.

## Features

- Fetch conversation IDs from Roblox Chat API.
- Retrieve and archive messages for each conversation.
- Save messages in HTML or TXT format.
- Simple command-line interface for interaction.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Ghosty-Tongue/RC-Saver/
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you have Python installed (Python 3.6+ recommended).
2. Update `cookies.json` with your Roblox security cookies.
3. Run `main.py` to start the script:
   ```
   python main.py
   ```
   
4. Follow the prompts to select conversations and save messages.

### Example

```
$ python main.py
Authenticated user ID: 1234567890
Select a username to fetch conversations:
1. example_username (Example Display Name)
Enter the number of the username to fetch conversations: 1
Selected username (display_name): example_username (Example Display Name)
Messages in conversation 987654321:
1. Hello! How are you?
2. I'm doing great, thanks!
Do you want to save these messages? (y/n): y
Enter 'txt' or 'html' to save as: txt
Messages saved to example_username_messages_20240707_165430.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
