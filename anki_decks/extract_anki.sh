ANKI_DIR=anki
CSV_DIR=csv

for f in "$ANKI_DIR"/*/*.anki*;
  do
    basename="$(dirname "$f")"
    basename="$(basename "$basename")"
    echo "${basename}""${f}"
    sqlite3 -csv "${f}" "SELECT * FROM notes;" > "$CSV_DIR/$basename.csv";
done