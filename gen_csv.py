"""\
Convert namespace from Schema.org-like JSON-LD to CSV.
"""

import argparse
import csv
import json
import sys
from pathlib import Path


IN_FN = "vocabulary.jsonld"
OUT_FN = "vocabulary.csv"


def to_csv(in_path, out_path):
    with open(in_path) as f:
        data = json.load(f)
    # for k, v in data.get("@context", {}).items():
    #     if v.startswith("http:"
    for entry in data["@graph"]:
        term = entry["@id"].strip().split("#", 1)[-1]
        type_ = entry["@type"].strip().split(":")[-1]
        assert type_ == "Class" or type == "Property"
        label = entry["rdfs:label"].strip()
        description = entry["rdfs:comment"].strip()
        domain = entry.get["rdfs:comment"].strip()

    with open(vocab_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            k = row["term"]
            add_terms[k] = f"{RO_TERMS_PREFIX}/{namespace}#{k}"
    return [ro_crate_context, add_terms]


def main(args):
    ns_dir = Path(args.ns_dir)
    vocab_path = ns_dir / VOCAB_FN
    if not vocab_path.is_file():
        raise RuntimeError(f"{vocab_path} not found")
    context = build_context(ns_dir.name, vocab_path,
                            ro_crate_version=args.ro_crate_version)
    if not args.output:
        args.output = ns_dir / "context.json"
    with open(args.output, "wt", encoding="utf8") as f:
        json.dump(context, f, ensure_ascii=False, indent=4, sort_keys=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ns_dir", metavar="NAMESPACE", help="namespace dir")
    parser.add_argument("-v", "--ro-crate-version", metavar="string",
                        default=RO_CRATE_VERSION, help="RO-Crate version")
    parser.add_argument('-o', '--output', metavar="FILE")
    main(parser.parse_args(sys.argv[1:]))
