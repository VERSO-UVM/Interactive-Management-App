import argparse
from app import app

# This must be True on the compute engine. It should be false for development.
REMOTE_SERVER = False


# @author Alyssa
# These are the CLI arguments that the ISM application accepts.
# Example:
# python wsgi.py --port=5001 --host=localhost --debug
def parse_it():
    parser = argparse.ArgumentParser(
        description='Start the ORCA ISM application')
    parser.add_argument('--debug', dest='debug', action='store_const',
                        const=True, default=False, help='Start in debug mode')
    parser.add_argument('--port', dest='port', action='store',
                        type=int, default=5000, help='Specify host port')
    parser.add_argument('--host', dest='host', action='store',
                        type=str, default='0.0.0.0', help='Specify host address')

    return parser.parse_args()


if __name__ == "__main__" and not REMOTE_SERVER:
    args = parse_it()
    app.run(debug=args.debug,
            port=args.port,
            host=args.host)

elif __name__ == "__main__":
    app.run(host="0.0.0.0")
