import os
from spotify_collage import app

if __name__ == '__main__':
    app.run(threaded=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("http://127.0.0.1", "5000").split(":")[-1])))