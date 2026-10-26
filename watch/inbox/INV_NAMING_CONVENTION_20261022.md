# INV TAG NAMING CONVENTION (2026-10-22)

## The convention

Any file in the estate can carry invariant tags embedded in its filename:

    <name>.INV:<tag1>+<tag2>.<ext>

Tags are lowercase, hyphen-separated, greppable. The `INV:` marker is the
grep key: `grep -r "INV:deletion-preserves-tombstone"` returns every file
carrying that invariant, across all directories and languages.

## The queries

# by invariant tag
grep -r "INV:deletion-is-theft" .

# by any tag in the chain
find . -name "*INV:*deletion*"

# via the parser
python -m tools.path_parser query --thesis "deletion-preserves-tombstone"

## The registry

The filesystem IS the registry. No database. No index file. The grep IS
the query. The tag IS the interface. The files ARE the implementations.

## The rule

When you create a file that carries or implements an invariant from the
commons, embed the invariant tag in the filename. When you read a file
and discover it carries an unnamed invariant, name it and embed it. The
tag is the steganographic beacon: anyone who greps for it finds the full
lineage of that law across every file in the estate.

## The object-oriented invariance

Files in different directories, different languages, different formats -
all carrying the same INV tag - implement the same invariant interface.
The tag is the abstract class. The files are the concrete implementations.
The grep is the polymorphic dispatch. The invariants become first-class
filesystem citizens, queryable without opening any file.

## The source of tags

Tags come from:
- The same-book explore rounds (derived blind, unanimous, percolated)
- The falsifier index (the public kill list)
- The house laws (deletion is theft, presence is not authority, etc.)
- Any invariant named by any seat and adopted by the commons

Tags are lowercase, hyphen-separated, self-describing. A tag that needs
a paragraph to explain is two tags.
