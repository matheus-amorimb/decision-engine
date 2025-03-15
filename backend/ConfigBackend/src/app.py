from fastapi import FastAPI

app = FastAPI()


@app.get('/health')
def health():
    return {'message': 'healthy'}


if __name__ == '__main__':
    health()
