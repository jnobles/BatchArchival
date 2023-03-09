# Building From Source

1. Create a virtual environment for the build and activate it

```
> python3 -m venv venv
> venv/bin/Scripts/activate.bat
```

2. Install needed requirements

```
(venv) > pip install -r requirements.txt
```

3. Build using the spec file

```
(venv) > pyinstaller build.spec
```
