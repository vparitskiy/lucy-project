import yaml
from yaml import CLoader as Loader


def read(src):
    """
    Name:               removeUnityTagAlias()

    Description:        Loads a file object from a Unity textual scene file, which is in a pseudo YAML style, and strips the
                        parts that are not YAML 1.1 compliant. Then returns a string as a stream, which can be passed to PyYAML.
                        Essentially removes the "!u!" tag directive, class type and the "&" file ID directive. PyYAML seems to handle
                        rest just fine after that.

    Returns:                String (YAML stream as string)


    """
    result = str()
    f = open(src, "r")

    for lineNumber, line in enumerate(f.readlines()):
        if line.startswith("--- !u!"):
            result += (
                "--- " + line.split(" ")[2] + "\n"
            )  # remove the tag, but keep file ID
        else:
            # Just copy the contents...
            result += line

    f.close()

    return result


def parse_importGridList(src, ja_col="Text", en_col="English"):
    data = yaml.load(read(src), Loader)
    for grid in data["MonoBehaviour"]["importGridList"]:

        # get 1st row to calculate row size

        strings = grid["rows"][0]["strings"]
        ja_index = strings.index(ja_col)
        en_idx = strings.index(en_col)
        max_idx = max(ja_index, en_idx)

        for row in grid["rows"][1:]:
            strings = row["strings"]
            if len(strings) <= max_idx:
                continue
            yield strings[ja_index], strings[en_idx]


def parse2(src, ja_col=0, en_col=1):
    data = yaml.load(read(src), Loader)
    for grid in data["MonoBehaviour"]["sheets"]:
        for row in grid["list"]:
            print(row)
            yield row["text"][ja_col], row["text"][en_col]
