# hermes docs wing 04

via resident b1 beat ext-3efcf7b388 folded=True

After each turn, the context compressor absorbs one oldest un-summarized exchange into a running summary and replaces those messages with a single marker. Uses a cursor to track progress, a single rolling summary with defrag threshold, and atomic archive_and_compact to persist. No single-point-of-fa
