# Tactical Lantern

A compact deterministic Python chess engine for the make.fun tiny-chess competition.

## Run

Python 3.13, standard library only. The competition supplies MAKEFUN_ENV_URL.

## Current status

The first online entry scored 876 Elo in practice. The second entry (01a1f3dd-99ee-74a2-9e0b-465155c756d9) uses a higher search budget and a 2.4-second search deadline. It scored one win, one draw, and four losses in the six-game local practice gauntlet, equivalent to 997 Elo under the published formula. All 246 moves were accepted. The longest move took 2.42 seconds. The platform reproduced 997 Elo with the same result and 119 spare plies. The final-entry floor is 1154 Elo.

These are experimental competition projects. No prize has been received.

## Repository contents

Source code, the MIT license, and the competition provenance anchor are included. Wallet private keys, API credentials, raw chat logs, transcript bundles, local output folders and machine-specific settings are excluded. Vendored competition helpers retain their original notices.

## License

MIT; see LICENSE.
