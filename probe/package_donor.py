"""Package locally installed shader objects; never distribute the generated bundle.

UnityPy 1.25.4. Reuse a genuine UnityFS container and its Shader type tree,
replacing its six shader records with byte-identical donor records. This is a
packaging experiment, not a claim of Unity runtime compatibility.
"""
import argparse
import hashlib
import json
from pathlib import Path

import UnityPy

SHADERS = (3602, 3604, 3761, 3633, 3622, 3620)
TEXTURES = {"soil.png": 2815, "rough.png": 3231, "wall.png": 441}
DONOR_HASH = "7c0c69bde01910dde60205bc1417cd56a39e27affd2de36735dcedd6facd6155"
TEMPLATE_HASH = "338146d78f42f9dff9917914e9191fbab4e197e6c3c186a415684715eb46d8e8"


def sha(data):
    return hashlib.sha256(bytes(data)).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--donor-data", type=Path, required=True)
    ap.add_argument("--template", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    donor_path = args.donor_data / "resources.assets"
    assert sha(donor_path.read_bytes()) == DONOR_HASH, "Donor build differs from the audited input"
    assert sha(args.template.read_bytes()) == TEMPLATE_HASH, "Container differs from the audited input"
    donor = UnityPy.load(str(donor_path))
    template = UnityPy.load(str(args.template))
    src = {o.path_id: o for o in donor.objects if o.path_id in SHADERS}
    slots = sorted((o for o in template.objects if o.type.name == "Shader"),
                   key=lambda o: o.path_id)
    assert len(slots) == len(SHADERS) == len(src), "Unexpected donor/template schema"
    manifest = {"donor_sha256": sha(donor_path.read_bytes()),
                "template_sha256": sha(args.template.read_bytes()), "shaders": []}
    for slot, source_id in zip(slots, SHADERS):
        source = src[source_id]
        parsed = source.read()
        assert parsed.m_Script is None and parsed.platforms == [4]
        assert not parsed.m_Dependencies, "Unresolved shader dependencies"
        raw = source.get_raw_data()
        slot.set_raw_data(raw)
        # set_raw_data stages bytes for save; read() still reads the original
        # stream. Validate the actual saved container below, not that old stream.
        manifest["shaders"].append({"name": parsed.m_ParsedForm.m_Name,
            "source_id": source_id, "destination_id": slot.path_id,
            "raw_sha256": sha(raw), "program_sha256": sha(parsed.compressedBlob)})
    bundle = next(iter(template.files.values()))
    bundle_bytes = bundle.save(packer="lz4")
    assert bundle_bytes.startswith(b"UnityFS")
    output = args.output / "donor-shaders.bundle"
    output.write_bytes(bundle_bytes)
    reread = UnityPy.load(str(output))
    actual = {o.path_id: o for o in reread.objects if o.type.name == "Shader"}
    for entry in manifest["shaders"]:
        obj = actual[entry["destination_id"]]
        assert sha(obj.get_raw_data()) == entry["raw_sha256"]
        assert obj.read().m_ParsedForm.m_Name == entry["name"]
        assert sha(obj.read().compressedBlob) == entry["program_sha256"]
    manifest["bundle_sha256"] = sha(bundle_bytes)
    manifest["bundle_bytes"] = len(bundle_bytes)
    manifest["textures"] = []
    for filename, path_id in TEXTURES.items():
        obj = next(o for o in donor.objects if o.path_id == path_id)
        texture = obj.read()
        texture.image.save(args.output / filename)
        manifest["textures"].append({"file": filename, "source_id": path_id,
            "name": texture.m_Name, "width": texture.m_Width, "height": texture.m_Height})
    for obj in donor.objects:
        if obj.type.name == "Texture2D" and "treeoaka" in (obj.peek_name() or "").lower():
            texture = obj.read()
            texture.image.save(args.output / "plant.png")
            manifest["textures"].append({"file": "plant.png", "source_id": obj.path_id,
                "name": texture.m_Name, "width": texture.m_Width, "height": texture.m_Height})
            break
    assert (args.output / "plant.png").is_file(), "TreeOakA not found"
    (args.output / "package.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
