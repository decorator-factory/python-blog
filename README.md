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