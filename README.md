# nxDumpMerger
Simple merger for Nintendo Switch dumped content, designed to merge dumps from nxdumptool.

# Important
The python script is writen in Python 3, use the "python3" command instead of "python" when use this program. Tkinter is bundled with a regular Python 3 install, so there's no need to install that. 

## Supported filename formats

- `file.ns0`, `file.ns1`, etc
- `file.nsp.00`, `file.nsp.01`, etc
- `file.xc0`, `file.xc1`, etc
- `file.xci.00`, `file.xci.01`, etc
- `folder/00`, `folder/01`, etc
  - This will output a .nsp file

Please [report any issues](https://github.com/emiyl/nxDumpMerger/issues) found.

The script is written in Python with tkinter, however a Windows version is included within the [releases](https://github.com/emiyl/nxDumpMerger/releases) which shouldn't require installing Python or any additional libraries.
