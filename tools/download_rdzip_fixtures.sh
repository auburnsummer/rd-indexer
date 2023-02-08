#!/usr/bin/env bash

# For use in the vitals tests, downloads rdzip fixtures used in the snapshots.
# why not git lfs? bc github charges a lotta money for the bandwidth

set -Eeuo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

cd ../orchard/vitals/test/fixtures

wget -nc https://codex.rhythm.cafe/know-you-2zRJRCjPqJx.rdzip
wget -nc https://codex.rhythm.cafe/rgb-7krFijAGF4D.rdzip
wget -nc https://codex.rhythm.cafe/pull-EpgEYcGYPnU.rdzip
wget -nc https://codex.rhythm.cafe/swing-c2QGYcw8GLq.rdzip
wget -nc https://codex.rhythm.cafe/sol-e-ma-dVMtiNt856v.rdzip
wget -nc https://codex.rhythm.cafe/ennui-og-3VFE7LSmzSo.rdzip
wget -nc https://codex.rhythm.cafe/one-forg-NqVywpSrZs1.rdzip
wget -nc https://codex.rhythm.cafe/one-uncu-eqSkB1ZX7Xz.rdzip
wget -nc https://cdn.discordapp.com/attachments/439363565007142912/1040242016593920030/Samario_Making_A_Mistake_-_One_Uncued_Tresillo2.rdzip
wget -nc https://cdn.discordapp.com/attachments/439363565007142912/1040248915414503464/auburnsummer_-_Triplet_Testaaaaa1.rdzip
wget -nc https://codex.rhythm.cafe/yi-xiao-Hg3afme47nr.rdzip
wget -nc https://codex.rhythm.cafe/banas-QbMoyaG2nfK.rdzip
wget -nc https://codex.rhythm.cafe/jimmy-s-Ccby1RK3XJK.rdzip