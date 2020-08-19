# nxDumpMerger
Simple merger for Nintendo Switch dumped content, designed to merge dumps from nxdumptool.

For NSP parts, dumps should be in format game.nsp/00, game.nsp/01, game.nsp/02 and so on, where game.nsp is a folder.
For XCI parts, dumps should be in format game.xc0, game.xc1, game.xc2 and so on.

This application was quickly chucked together in an afternoon and may have several bugs, which is why I have labelled this pre-release. Please [report any bugs](https://github.com/emiyl/nxDumpMerger/issues) or situations where the application has failed so I can improve this.

The script is written in Python and requires tkinter to run, however a Windows version is included within the [releases](https://github.com/emiyl/nxDumpMerger/releases) which shouldn't require installing Python or any additional libraries.
