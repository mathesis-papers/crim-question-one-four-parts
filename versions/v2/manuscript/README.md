# Four-part CRIM: an alternative proof after Mehat (2026)

This package answers Bašić–Gottlieb–Krnc (2026), *CRIM: A Natural Game on
Integer Partitions*, arXiv:2606.16828v1, Section 5, Question 1, p. 17.
For positive integers `a >= b >= c >= d`, losing positions have even `a`
and satisfy the disjoint table in Theorem 1 of `note.tex`.
Mehat's earlier proof is Theorem 4 of the manuscript in his 23 August 2026
archive, DOI `10.5281/zenodo.22070744`. The note supplies a direct induction
and thirteen explicit winning moves, small-row hook-stacking closure,
odd-gap consequences through six rows or columns using Mehat's rank theorem,
and exact one- and two-part padding formulas. The corrected three-part
criterion is also credited to Mehat's Corollary 25 and Section 12.

## Contents

- `note.tex`: self-contained statement, proof, winning moves and consequences.
- `note.pdf` (companion file): readable mathematical note.
- `metadata.json`: title, creators, license, problem identifier and scientific links.
- `verify.py`: standard-library exact finite checker.
- `checker-output.json` (companion file): the output for largest part at most 30 and at most four parts.
- `LICENSE.txt`: license identifier and canonical terms.

## Build

Use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively use a standard LaTeX installation with the packages named in
`note.tex`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is included in the TeX source; no external `.bib` file is needed.

## Exact finite checks

Requires Python 3.9 or later and no third-party packages.

```sh
python3 verify.py --max-part 30 > checker-output.json
```

The output has status `ALL_CHECKS_OK`, 46,376 positions, 40,920 four-part
positions, 15,761 losing four-part positions and all thirteen strategy cases.
Additional checks compare Mehat's parity table, cover 7,149 hook stacks and
their conjugates, and confirm the 38 Appendix A positions.
The output SHA256 is recorded in `MANIFEST.sha256`.
The source archive contains five text/source files, the checker output and their SHA256 manifest; the companion PDF and
regenerable checker output accompany it separately.
The source-move evaluator uses conjugation and row deletion rather than the
classification to compute Grundy values. A second move implementation uses
column heights, and their complete follower sets are compared.
The finite range supplements the unrestricted written proof; it is not an
all-size enumeration.

## Mathematical coverage

The theorem gives every zero Grundy value on four positive parts. The corrected
three-part condition excludes the all-one column `[1,1,1]`. Written consequences
give losing-hook stacking through four rows or columns, first-row/first-column
winning moves and odd gaps through six rows or columns using Mehat's rank
theorem, and one- and two-part padding and appended-unit-part formulas.
The square-rectair formula is corrected at its one-cell boundary.
General nonzero Grundy formulas and misère Conway pairs are outside
this coverage.

The declaration `D5.S3.Combinatorics.Games.CrimFourPartClassification.result`
states the unrestricted four-part equivalence in the pinned file:

https://github.com/the-omega-institute/trureturing/blob/e0da8fcc80226febc4e7ea0836927bc71d158292/D5/S3/Combinatorics/Games/CrimFourPartClassification.lean

The game definitions and mex recursion are in:

https://github.com/the-omega-institute/trureturing/blob/e0da8fcc80226febc4e7ea0836927bc71d158292/D5/S0/Certificates/Games/CrimGrundyRefutation.lean

That file's separate `result` negates the near-square formula at
`r=7,k=5`, outside this note's coverage. The square boundary declaration
`D5.S0.Certificates.Games.CrimRectairSquareBoundaryRefutation.result`
negates the printed universal square-rectair formula using `r=1,k=0`:

https://github.com/the-omega-institute/trureturing/blob/e0da8fcc80226febc4e7ea0836927bc71d158292/D5/S0/Certificates/Games/CrimRectairSquareBoundaryRefutation.lean

The lower-row classification and consequences have written proofs in the note.

## Authors and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

CC BY 4.0 (`cc-by-4.0`). See `LICENSE.txt`.
