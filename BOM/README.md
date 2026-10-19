# Bill of Materials

The consolidated BOM is generated from the nine module-level BOM exports in
`../electronics/output/bom/`.

| File | Contents |
|---|---|
| `bill_of_materials.csv` | Normalized line items for all nine PCB modules |
| `bom_summary.csv` | Per-module line count, part count and known cost |

## Cost note

Known prices cover connectors, passive components, LEDs and a few ICs only. The
nine BOM files list 48 line items and 57 parts with a known total of **CNY 31.44**.
Sixteen lines have no price, including the RP2040/Pico module, LoRa modem, GNSS
module, MQ sensors and several connectors. The true cost is therefore higher.

No supplier links or date-stamped quotes are included in the archive. Treat the
prices as historical reference values from the 2023-08-15 exports, not current
procurement data.
