ANKI_DIR=anki
APKG_DIR=apkg

for f in "$APKG_DIR"/*.apkg;
  do
    basename="$(basename "$f")"
    unzip -j "$f" collection.anki* -d "$ANKI_DIR"/"$basename"
done