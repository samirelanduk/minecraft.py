# minecraft.py

A tool for dealing with Minecraft saves.

## Use

To initialise a save for backing up:

```
python minecraft.py init --name save_name
```

To continuously watch all initialised saves and commit when 10 minutes has passed:

```
python minecraft.py watch
```

To do the same but after fice minutes:

```
python minecraft.py watch --wait 5
```

To do one check of all save files:

```
python minecraft.py save
```

To do one check of a specific save file:

```
python minecraft.py save save_name
```