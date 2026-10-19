"""Snapshot user-profile hashes and restore only Unity preference changes.

Registry recovery is intentional: Unity can save display preferences even in a
batch graphics test. No normal save/settings files are copied or modified.
"""
import argparse
import base64
import hashlib
import json
import re
from pathlib import Path
import winreg

KEY = r"Software\Freehold Games\CavesOfQud"
PROFILE = Path.home() / "AppData/LocalLow/Freehold Games/CavesOfQud"


def prefs():
    result = {}
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY) as key:
            for i in range(winreg.QueryInfoKey(key)[1]):
                name, value, kind = winreg.EnumValue(key, i)
                result[name] = [kind, base64.b64encode(value).decode() if isinstance(value, bytes) else value]
    except FileNotFoundError:
        pass
    return result


def files():
    return {str(p.relative_to(PROFILE)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in PROFILE.rglob("*") if p.is_file()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["before", "after"])
    ap.add_argument("--root", type=Path, required=True)
    args = ap.parse_args()
    baseline = args.root / "profile-before.json"
    if args.mode == "before":
        assert not baseline.exists(), "Preserve the original baseline across repeated runs"
        baseline.write_text(json.dumps({"registry": prefs(), "files": files()}, indent=2), encoding="utf-8")
        print("Normal profile baseline recorded")
        return
    before = json.loads(baseline.read_text(encoding="utf-8"))
    after = prefs()
    changed = sorted(k for k in before["registry"].keys() | after.keys()
                     if before["registry"].get(k) != after.get(k))
    if changed:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, KEY) as key:
            for name in changed:
                if name not in before["registry"]:
                    winreg.DeleteValue(key, name)
                else:
                    kind, value = before["registry"][name]
                    if kind == winreg.REG_BINARY:
                        value = base64.b64decode(value)
                    winreg.SetValueEx(key, name, 0, kind, value)
    current = files()
    changed_files = sorted(k for k in before["files"].keys() | current.keys()
                           if before["files"].get(k) != current.get(k))
    # Qud's Logger uses the native Unity profile even with explicit save paths.
    # Classify observed runtime diagnostics separately; never ignore saves/options.
    diagnostics = [p for p in changed_files if re.fullmatch(
        r"(?:game_log(?:\.\d+)?\.txt|build_log\.txt(?:\.prev)?|Unity\\ShaderVariantAnalytics\\ShaderRuntimeInfoEvent\.json|"
        r"Unity\\3bf6c570-214f-4f5a-bfcc-196732543d03\\Analytics\\.*)", p)]
    protected_changes = [p for p in changed_files if p not in diagnostics]
    report = {"normal_profile_file_count": len(current), "changed_normal_profile_files": changed_files,
              "changed_runtime_diagnostics": diagnostics, "changed_save_or_settings_files": protected_changes,
              "diagnostic_changes": {
                  "created": sum(p not in before["files"] for p in diagnostics),
                  "removed": sum(p not in current for p in diagnostics),
                  "modified": sum(p in before["files"] and p in current for p in diagnostics)},
              "restored_unity_preference_count": len(changed), "preferences_restored": prefs() == before["registry"]}
    (args.root / "preservation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    assert not protected_changes and report["preferences_restored"]


if __name__ == "__main__":
    main()
