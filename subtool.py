#!/usr/bin/env python

import sys
import argparse
import lib as subtool


def main(argv=None):
    args = (argv or sys.argv)[0]

    parser = argparse.ArgumentParser(description="Easily fetch, build, deploy a subreddit design",
            usage="%(prog)s [options] <command>")
    subparser = parser.add_subparsers(dest="command")

    # FETCH
    fetch = subparser.add_parser("fetch", help="Fetch assets from a subreddit")

    fetch.add_argument("subreddit",
                        type=unicode,
                        help="Subreddit name")

    fetch.add_argument("--images", "-I",
                        dest="fetch_images",
                        action="store_true",
                        help="Fetch images")

    fetch.add_argument("--no-images",
                        dest="fetch_images",
                        action="store_false",
                        default=False,
                        help="Ignore images")

    fetch.add_argument("--stylesheet", "-s",
                        dest="fetch_stylesheet",
                        action="store_true",
                        default=True,
                        help="Fetch stylesheet")

    fetch.add_argument("--no-stylesheet",
                        dest="fetch_stylesheet",
                        action="store_false",
                        help="Ignore stylesheet")

    fetch.set_defaults(func=subtool.fetch)

    # PUSH
    push = subparser.add_parser("push", help="Push assets to a subreddit")

    push.add_argument("subreddit",
                        type=unicode,
                        help="Subreddit name")

    push.add_argument("--images", "-I",
                        dest="push_images",
                        action="store_true",
                        help="Push images")

    push.add_argument("--no-images",
                        dest="push_images",
                        action="store_false",
                        default=False,
                        help="Ignore images")

    push.add_argument("--force",
                        dest="push_force",
                        action="store_true",
                        default=False,
                        help="Ignore existing images")

    push.add_argument("--stylesheet", "-s",
                        dest="push_stylesheet",
                        action="store_true",
                        default=True,
                        help="Push stylesheet")

    push.add_argument("--no-stylesheet",
                        dest="push_stylesheet",
                        action="store_false",
                        help="Ignore stylesheet")

    push.set_defaults(func=subtool.push)

    # Build
    build = subparser.add_parser("build", help="Build sprites and stylesheets")
    build.set_defaults(func=subtool.build)

    # Merge
    merge = subparser.add_parser("merge", help="Merge built file into design")
    merge.set_defaults(func=subtool.merge)


    args = parser.parse_args()
    if args.command == "fetch":

        kwargs = {
            "fetch_stylesheet": args.fetch_stylesheet,
            "fetch_images": args.fetch_images,
        }

        args.func(args.subreddit, **kwargs)

    if args.command == "push":

        kwargs = {
            "push_stylesheet": args.push_stylesheet,
            "push_images": args.push_images,
            "force": args.push_force
        }

        args.func(args.subreddit, **kwargs)

    if args.command == "build":

        args.func()

    if args.command == "merge":

        args.func()

if __name__ == "__main__":
    sys.exit(main())
