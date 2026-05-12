from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(title="Collaborative Video AI Agents API")
    
    @app.get("/health")
    def health_check() -> dict[str, str]:
        return {
            "status": "ok",
            "service": "api-gateway"
        }
        
    return app


app = create_app()