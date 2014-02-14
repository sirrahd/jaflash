# jaflash Japanese flashcards

I use these flashcard sets for studying Japanese vocabulary and kanji with [Anki](http://ankisrs.net/).

Sets are manually typed tab-delimited files in the raw/ directory. The structure of content in raw/ is reading, kanji (optional), and English meaning.

The make.py script prepares this data for importing to Anki. Vocab structure becomes Kanji (if available) or reading, reading (if Kanji was not available), English meaning. Kanji structure becomes kanji, then reading and meaning separated by a space.

This allows Anki to easily create vocabulary flashcards that show kanji or reading on one side, then meaning and reading on the other, and kanji flashcards that show meaning and reading on one side, then kanji on the other.