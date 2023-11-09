import argparse
from app import app

## @author Alyssa
# These are the CLI arguments that the ISM application accepts.
# Example:
# python wsgi.py --port=5001 --host=localhost --debug
parser = argparse.ArgumentParser(description='Start the ORCA ISM application')
parser.add_argument('--debug', dest='debug', action='store_const', const=True, default=False, help='Start in debug mode')
parser.add_argument('--port', dest='port', action='store', type=int, default=5000, help='Specify host port')
parser.add_argument('--host', dest='host', action='store', type=str, default='0.0.0.0', help='Specify host address')

args = parser.parse_args()

if __name__ == "__main__":
    app.run(debug=args.debug,
            port=args.port,
            host=args.host)
