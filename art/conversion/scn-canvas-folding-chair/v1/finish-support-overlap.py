"""Place the near support end inside the sling silhouette, retaining the draft."""
from pathlib import Path
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent
svg=(HERE/'constructed-front-v2.svg').read_text(encoding='utf-8')
old='M3.05 9.45L6.5 17.95V18.5H6.05L2.65 9.7Z';new='M3.05 8.6L6.5 17.95V18.5H6.05L2.65 8.85Z'
assert old in svg;svg=svg.replace(old,new)
(HERE/'constructed-front-v3.svg').write_bytes(svg.encode());(HERE/'constructed-front-v3.png').write_bytes(svg_to_bytes(svg_string=svg))
print('Near support end now lies inside the sling coverage; earlier two construction drafts retained.')
