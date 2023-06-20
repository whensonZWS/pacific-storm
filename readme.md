# Pacific Storm Survival
## Introduction
Pacific Storm Survival is a custom game map made for Mental Omega, a Red Alert 2 mod. 3 Players must survive against waves of enemy while protecting their psychic beacon from destruction. The map features different factions of enemy, randomized objectives and enemy waves with increasing intensity over time.

## Preview
Coming Soon

## Project Goals
Custom Red Alert maps with objectives are fun to play with friends, but they often lack replaybility. This map project is an attempt to alleviate this issue by introducing some mild random elements to the objectives and enemy composition.

This map project is also an attempt to streamline triggers editing process in Final Alert. Despite being a well-rounded Red Alert map editor, Final Alert GUI is not modern enough and its triggers editing experience is not the best. I find writing triggers scripts in a pre-defined format in yaml more manageable than the drop-down-list-hell in Final Alert GUI, though this requires a good understanding in the specification of Red Alert Map files.

## Build
To build map, in root directory, run
```bash
python ./waves/team-gen.py
python ./waves/trigger-gen.py
python ./tools/mod-merge.py
```
The result should resides within `./dist`

## Custom Tasks Scripts for VS Code
Coming Soon.