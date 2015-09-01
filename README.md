# tagpro-subreddit-css

A repository for building and deploying the TagPro
subreddit design.

## Overview

This project uses Python 2.7 to fetch, build, and push
the design to a subreddit.

#### Setup

`pip install -r requirements.txt`

#### Usage

This project has a `subtool` command which is used
to fetch, build, and push changes to the subreddit.

For general help:
`./subtool -h`

##### Fetch

To fetch the latest style from the subreddit, use the `fetch`
sub-command.

`./subtool fetch`

##### Push

To push changes to the subreddit, use the `push` sub-command.

`./subtool push`
