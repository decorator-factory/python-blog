# Running the blog

## 1. Install frontend dependencies

```bash
cd frontend/
npm install
```

## 2. Build the frontend bundle

```bash
npm run build
```

## 3. Install backend dependencies
```bash
cd ..
python3.9 -m venv env
env/bin/pip install -r requirements.txt
```

## 4. Run the server

### ...for development
```bash
env/bin/uvicorn server:app --reload
```

### ...for production
```bash
env/bin/uvicorn server:app --port 80
```


# Running the tests

## 0. Make sure you're in the repo's root directory

## 1. Install `pytest`

```bash
env/bin/pip install pytest
```

## 2. Run `pytest`
```bash
env/bin/python -m pytest
```

## (optional) 3. Generate coverage:
```bash
env/bin/pip install coverage
env/bin/python -m coverage run --omit **/env/* -m pytest
env/bin/python -m coverage html
```
Then you should see an `htmlcov` directory