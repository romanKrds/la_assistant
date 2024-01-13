from la_assistant import create_app
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

if __name__ == '__main__':
    app = create_app()
    # TODO: bind debug flag to env variable
    app.run(debug=True)
