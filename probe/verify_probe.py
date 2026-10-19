"""Verify retained engine evidence and private PNG readbacks (requires Pillow)."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image


def read(root, name):
    return json.loads((root / name).read_text(encoding="utf-8"))


def verify(root):
    shaders = read(root, "loaded-shaders.json")
    renders = read(root, "shader-renders.json")
    capture = read(root, "capture.json")
    preservation = read(root, "preservation.json")
    assert len(shaders) == 6 and all(s["isSupported"] and s["passes"] == 1 for s in shaders)
    assert read(root, "runtime.json")["graphics"] == "Direct3D11"
    assert read(root, "finished.json")["exitCode"] == 0
    assert read(root, "capture-finished.json")["exitCode"] == 0
    assert len(renders) == 11
    images = {}
    for result in renders:
        png = root / (result["test"] + ".png")
        with Image.open(png) as im:
            assert im.size == (128, 128)
            rgb = im.convert("RGB").tobytes()
        assert result["supported"] and result["nonBackgroundPixels"] > 1000 and result["pinkPixels"] == 0
        assert not any(r > 220 and g < 30 and b > 220 for r, g, b in zip(rgb[0::3], rgb[1::3], rgb[2::3]))
        images[result["test"]] = rgb
    changes = {}
    for base, altered in [("Custom_Terrain_hard", "tint"), ("Custom_Terrain_fade", "edge"),
                          ("Custom_Terrain_fade_rough", "edge"), ("Custom_Plant_cutout", "wind"),
                          ("Custom_Plant_transparent", "wind")]:
        a, b = images[base + "_base"], images[base + "_" + altered]
        changed = sum(a[i:i+3] != b[i:i+3] for i in range(0, len(a), 3))
        assert changed > 100, (base, changed)
        changes[base + "_" + altered] = changed
    assert capture["selectionHook"] and capture["publicationHook"]
    frames = capture["frames"]
    assert [f["phase"] for f in frames] == ["baseline", "late-buffer-mutation", "actor-moved"]
    assert [f["generation"] for f in frames] == [1, 2, 3]
    for f in frames:
        assert f["publishInsideBufferLock"] and f["consumeInsideBufferLock"] and f["matchesSubmitted"]
        assert f["submittedHash"] == f["consumedHash"]
        assert f["producerThread"] != f["consumerThread"] and f["consumerThread"] == 1
    cells = [{(c["x"], c["y"]): c for c in f["cells"]} for f in frames]
    for xy, expected in {(8, 8): "DirtPath", (9, 8): "BrinestalkWall", (10, 8): "Watervine",
                         (11, 8): "WatervineFarmerJoppa", (12, 8): "Pond"}.items():
        assert cells[0][xy]["source"] == expected
        assert cells[0][xy]["resolved"] == cells[0][xy]["submitted"]
    assert cells[0][(13, 8)]["source"] == "DirtPath"  # Invisible actor is not exposed.
    assert not cells[0][(14, 8)]["visible"] and cells[0][(14, 8)]["source"] is None
    assert cells[1][(10, 8)]["requiresOriginal"]
    assert sum(c["requiresOriginal"] for c in frames[1]["cells"]) == 1
    assert cells[2][(11, 8)]["source"] == "DirtPath"
    assert cells[2][(11, 9)]["source"] == "WatervineFarmerJoppa"
    assert preservation["preferences_restored"] and not preservation["changed_save_or_settings_files"]
    return {"donor_shaders_loaded_and_rendered": 6, "pixel_readbacks": 11,
            "changed_pixels_by_material_test": changes, "paired_scene_frames": 3,
            "visibility_exclusion": True, "actor_movement": True, "late_mutation_detected": True,
            "capture_view": frames[0]["view"],
            "limits": ["Controlled Qud object fixture, not a generated or saved Joppa session",
                       "Captured during MainMenu boot; gameplay view/input gating untested",
                       "No complete replacement renderer or arbitrary-mod compatibility claim"],
            "normal_saves_and_settings_unchanged": True,
            "unity_preferences_restored": True,
            "runtime_diagnostic_changes": preservation["diagnostic_changes"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    result = verify(args.root)
    # JSON metadata is normalized by Git. Bind its content independently of CRLF.
    result["evidence_hash_format"] = "SHA256 of UTF-8 sorted compact JSON"
    result["evidence_hashes"] = {p.name: hashlib.sha256(json.dumps(read(args.root, p.name),
        sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        for p in sorted(args.root.glob("*.json")) if p.name != "profile-before.json"}
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
