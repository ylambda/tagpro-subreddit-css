import os
import re
import urllib
import urlparse

import praw
from glue.bin import main as glue
from csscompressor import compress

reddit = None
def reddit_login():

    global reddit
    credentials = {
        "username": os.environ.get("REDDIT_USERNAME"),
        "password": os.environ.get("REDDIT_PASSWORD"),
    }

    r = praw.Reddit("Subreddit stylesheet tool by /u/ylambda, run by /u/%s" % credentials["username"])
    r.login(**credentials)
    reddit = r


def fetch(subreddit_name,
        fetch_stylesheet=True, fetch_images=False):
    """
    Fetch assets from a subreddit
    """

    # Setup
    if reddit is None:
        reddit_login()
    original_decode = reddit.config.decode_html_entities
    reddit.config.decode_html_entities = True

    # Make sure the destination exists
    destination = "build"
    try:
        os.makedirs(destination)
    except OSError:
        if not os.path.isdir(destination):
            raise

    subreddit = reddit.get_subreddit(subreddit_name)
    style = subreddit.get_stylesheet()

    # Save Stylesheet
    if fetch_stylesheet:
        print "Downloading stylesheet."
        stylesheet = style.get("stylesheet")
        f = open(os.path.join(destination, "stylesheet.css"), "w")
        f.write(stylesheet)
        f.close()

    # Save Images
    if fetch_images:
        image_dir = os.path.join(destination, "images")
        try:
            os.makedirs(image_dir)
        except OSError:
            if not os.path.isdir(image_dir):
                raise

        for image in style.get("images"):
            print "Downloading image: %s" % image.get("name")
            image_path = urlparse.urlparse(image.get("url")).path
            image_uid, image_extension = os.path.splitext(image_path)

            image_filename = os.path.join(image_dir, "%s%s" % (
                image.get("name"), image_extension))

            urllib.urlretrieve(image.get("url"), image_filename)

    # Teardown
    reddit.config.decode_html_entities = original_decode

    print "Done."

def push(subreddit_name,
        push_stylesheet=True, push_images=False, force=False):
    """
    Push a directory to a subreddit
    """

    # Setup
    source = "build"
    if not os.path.isdir(source):
        raise Exception

    if reddit is None:
        reddit_login()
    subreddit = reddit.get_subreddit(subreddit_name)
    style = subreddit.get_stylesheet()


    # Push images
    if push_images:
        image_dir = os.path.join(source, "images")
        if not os.path.isdir(image_dir):
            raise Exception

        images = set()
        # Get existing images on the subreddit
        if not force:
            print "Checking subreddit for existing images."
            for image in style.get("images"):
                image_path = urlparse.urlparse(image.get("url")).path
                image_uid, image_extension = os.path.splitext(image_path)

                image_filename = "%s%s" % (
                    image.get("name"), image_extension)

                # Strip off first slash
                images.add(image_filename)

        # Uploading images
        for image_filename in os.listdir(image_dir):
            image_path = os.path.join(image_dir, image_filename)
            if os.path.isfile(image_path):
                if not image_filename in images:
                    image_name = os.path.splitext(image_filename)[0]
                    print "Uploading %s" % image_name
                    subreddit.upload_image(image_path, image_name)

    # Upload Stylesheet
    if push_stylesheet:
        print "Uploading stylesheet."
        stylesheet = open(os.path.join(source, "stylesheet.css"), "r")
        subreddit.set_stylesheet(stylesheet.read())
        stylesheet.close()

    print "Done."

def build():
    """
    Build sprites and stylesheets
    """
    import glob


    # Build sprites
    source_dir = "design/sprites"
    image_dir = "build/images"
    css_dir = "build/css"
    glue_options = "glue --source=%s --project --css=%s --img=%s" % (source_dir, css_dir, image_dir)
    glue_args = glue_options.split()
    glue(argv=glue_args)

    f = open("design/stylesheet.css", "r")
    stylesheet = f.read()
    f.close()

    # Insert sprites stylesheets
    css_files = glob.glob("build/css/*.css")
    for css_file in css_files:
        with open(css_file, "r") as f:
            css_basename = os.path.splitext(os.path.basename(css_file))[0]
            search_string = "/* --- INSERT BUILD %s --- */" % css_basename.upper()
            insert_point = stylesheet.find(search_string)

            if insert_point > -1:
                print "Adding %s to stylesheet" % css_file
                build_style = "/* --- BUILD START %s --- */\n" % css_basename.upper()
                build_style += compress(f.read())
                build_style += "\n/* --- BUILD END %s --- */\n" % css_basename.upper()
                stylesheet = stylesheet.replace(search_string, build_style)
            f.close()

    f = open("build/stylesheet.css", "w")
    f.write(stylesheet)
    f.close()

    print "Done."

def merge():
    """
    Merge built stylesheet into design
    """

    f = open("build/stylesheet.css", "r")
    stylesheet = f.read()
    f.close()

    # Find Built sections and replace with insert lines
    build_start = r"/\* --- BUILD START ([-\w]+) --- \*/"
    build_end = "\n/* --- BUILD END %s --- */\n"

    while re.search(build_start, stylesheet) != None:
        start_match = re.search(build_start, stylesheet)
        insert_string = "/* --- INSERT BUILD %s --- */" % start_match.group(1)
        end_match = build_end % start_match.group(1)
        end_match_index = stylesheet.find(end_match) + len(end_match)
        stylesheet = stylesheet[:start_match.start()] + insert_string + stylesheet[end_match_index:]

    f = open("design/stylesheet.css", "w")
    f.write(stylesheet)
    f.close()
