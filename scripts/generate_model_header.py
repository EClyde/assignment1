"""Convert outputs/surfaces.npz to Arduino PROGMEM model.h."""
from pathlib import Path
import json
import numpy as np

d=np.load("outputs/surfaces.npz")
tables=d["tables"]
n=int(d["grid_n"])
names=[str(k) for k in d["class_names"]]
bounds=d["bounds"]
tau=float(d["reject_tau"])
lines=["#pragma once","#include <Arduino.h>","#include <pgmspace.h>",
       "#define GRID_N "+str(n),"#define NUM_CLASSES "+str(len(names)),
       "#define REJECT_TAU "+repr(tau)+"f",
       "const uint8_t CLASS_TABLE[NUM_CLASSES][GRID_N][GRID_N] PROGMEM = {"]
for table in tables:
    lines.append("{")
    for row in table:
        lines.append("{"+",".join(map(str,row.tolist()))+"},")
    lines.append("},")
lines.extend(["};","const float SCALE_BOUNDS[4] = {"+",".join(f"{float(x):.9g}f" for x in bounds)+"};",
              "const char* const CLASS_NAMES[NUM_CLASSES] = {"+",".join(json.dumps(s) for s in names)+"};"])
dest=Path("firmware/inference/model.h")
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text("\n".join(lines)+"\n")
print(f"Generated {dest}, {tables.size} table bytes + 16 bounds bytes")
