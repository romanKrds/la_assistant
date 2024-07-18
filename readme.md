# Language Learning Assistant - Flask App

This Flask application is designed to help users study foreign languages with the assistance of the OpenAI API. The app provides an interactive platform where users can communicate with an AI assistant to improve their language skills.

## Features

- **Interactive Communication**: Users can engage in conversations with the AI assistant, enhancing their language learning experience through practice and feedback.
- **Error Checking**: The app checks user messages for grammatical and usage errors, providing real-time corrections and suggestions.
- **Message Storage**: User messages are saved, allowing for future review and progress tracking.
- **Review System**: Users can review their previous messages and corrections to reinforce their learning.

## Code Structure

- The core functionality of the assistant is implemented in the `assistant` blueprint, which handles communication with the OpenAI API and processes user interactions.

## Setup and Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -e .
    ```

4. Set up environment variables (create a .env file with following variables):
    ```bash
    IS_DEV_MODE
    OPENAI_API_KEY
    OPENAI_ASSISTANT_ID
    REPETITIONS_TO_MEMORIZE_WORD_NUMBER
    MEMORIZE_WORD_SET_LENGTH
    ```

5. Run the Flask application:
    ```bash
    flask run --app la_assistant
    ```
   Access the app by navigating to `http://127.0.0.1:5000` in your web browser.

## Contributing

We welcome contributions to enhance the functionality and features of this language learning assistant. Feel free to open issues and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
