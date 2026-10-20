"""Translate existing human layers to one shared canvas anchor; preserve v1 art.

No generation, rescaling, anatomy edits or native test is performed here.
Run separately for each ledger entry, then inspect its registration plate.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
CANVAS = (512, 1024)
CONTACT = (256, 950)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path):
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)}


def save_json(path, value):
    path.write_bytes((json.dumps(value, indent=2) + "\n").encode())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("family", choices=["human-male", "human-female", "human-male-older"])
    args = parser.parse_args()
    base = ROOT / "art/conversion" / ("body-" + args.family)
    source, target = base / "v1", base / "v2"
    target.mkdir(exist_ok=True)
    assert not (target / "model.json").exists(), "Do not overwrite recorded registration"
    model = json.loads((source / "model.json").read_text(encoding="utf-8"))
    revised = copy.deepcopy(model)
    inputs = [record(source / "model.json"), record(Path(__file__).resolve())]
    outputs, decisions, assemblies = [], {}, []
    for facing, rows in revised["views"].items():
        old_contact = tuple(rows[0]["contact"])
        assert all(tuple(row["contact"]) == old_contact for row in rows)
        dx, dy = (CONTACT[i] - old_contact[i] for i in range(2))
        assembly = Image.new("RGBA", CANVAS)
        decisions[facing] = {"old_contact": old_contact, "translation": [dx, dy], "new_contact": CONTACT, "layers": {}}
        for row in sorted(rows, key=lambda r: r["layer"]):
            for name in [f'{row["component"]}-{facing}.png', f'{row["component"]}-mask-{facing}.png']:
                path = source / name
                image = Image.open(path)
                assert image.size == CANVAS
                bounds = (image.getchannel("A") if image.mode == "RGBA" else image).getbbox()
                assert bounds is not None
                moved_bounds = (bounds[0] + dx, bounds[1] + dy, bounds[2] + dx, bounds[3] + dy)
                is_mask = "-mask-" in name
                if not is_mask:
                    assert 0 <= moved_bounds[0] < moved_bounds[2] <= CANVAS[0], (name, moved_bounds)
                    assert 0 <= moved_bounds[1] < moved_bounds[3] <= CANVAS[1], (name, moved_bounds)
                moved = Image.new(image.mode, CANVAS, 0)
                moved.paste(image, (dx, dy))  # Exact pixel translation; no alpha multiplication.
                # Authoring diagnostic: every visible source pixel survives byte-for-byte.
                # Source segmentation masks include full-canvas rectangles. Only
                # their portion covering source art is meaningful; padding may clip.
                relevant = Image.open(source / f'{row["component"]}-{facing}.png').getchannel("A").getbbox() if is_mask else bounds
                moved_relevant = tuple(v + (dx if i % 2 == 0 else dy) for i, v in enumerate(relevant))
                assert image.crop(relevant).tobytes() == moved.crop(moved_relevant).tobytes()
                moved.save(target / name)
                inputs.append(record(path))
                outputs.append(record(target / name))
                decisions[facing]["layers"][name] = {"before_bounds": bounds, "after_bounds": moved_bounds, "visible_pixels_preserved": True}
                if not is_mask:
                    assembly = Image.alpha_composite(assembly, moved)
                    row.update(file=f'{args.family}-v2-{name}', public_file=(target / name).relative_to(ROOT).as_posix(), sha256=sha(target / name))
            row.update(contact=list(CONTACT), center_x=0, center_z=(CONTACT[1] - CANVAS[1] / 2) * row["height"] / CANVAS[1])
        assembly.save(target / f"selected-{facing}.png")
        outputs.append(record(target / f"selected-{facing}.png"))
        assemblies.append((facing, assembly))
    revised["registration"] = {
        "version": 2, "canvas": CANVAS, "contact": CONTACT,
        "method": "Integer translation of body, head and masks together; no rescale or independent silhouette centering.",
        "source_model": record(source / "model.json"),
        "native_acceptance": "Deferred until all conversions are generated."
    }
    save_json(target / "model.json", revised)
    save_json(target / "registration-decisions.json", decisions)
    outputs.extend([record(target / "model.json"), record(target / "registration-decisions.json")])
    # Guides are report annotations only; the production PNGs stay transparent.
    plate = Image.new("RGB", (4 * 288, 650), "#142823")
    draw = ImageDraw.Draw(plate)
    font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 15)
    draw.text((18, 12), args.family + " / v2 / common contact (256, 950)", fill="#e3cf43", font=font)
    assemblies.append(("west (mirror)", ImageOps.mirror(dict(assemblies)["east"])))
    for column, (facing, assembly) in enumerate(assemblies):
        left, top = column * 288 + 16, 54
        tile = Image.new("RGBA", CANVAS, "#20382d")
        tile.alpha_composite(assembly)
        tile = tile.convert("RGB").resize((256, 512), Image.Resampling.LANCZOS)
        plate.paste(tile, (left, top))
        x, y = left + CONTACT[0] // 2, top + CONTACT[1] // 2
        draw.line((x, top, x, top + 511), fill="#cebc45", width=1)
        draw.line((left, y, left + 255, y), fill="#70b8b0", width=1)
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), outline="#fff6a0", width=2)
        draw.text((left, 578), facing.upper(), fill="#e3cf43", font=font)
    draw.text((18, 610), "Gold: canvas center/pivot. Teal: ground. Side profile may extend beyond center.", fill="#e5e8d8", font=font)
    plate.save(target / "registration-comparison.png")
    outputs.append(record(target / "registration-comparison.png"))
    save_json(target / "provenance.json", {"inputs": inputs, "outputs": outputs})
    print(json.dumps({"family": args.family, "translations": {f: d["translation"] for f, d in decisions.items()}, "plate": str(target / "registration-comparison.png")}))


if __name__ == "__main__":
    main()
