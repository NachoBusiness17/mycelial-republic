# Row: atlas-g1b

- **pointer**: /mag/mag/atlas.py
- **claim**: `python -m mag.atlas build` is a real CLI (argparse subcommand).
- **type**: gopher
- **confidence**: H
- **status**: VERIFIED
- **evidence**: atlas.py L66-72 defines argparse prog=mag.atlas with sub.add_parser("build") and routes to build().
