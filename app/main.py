import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from .providers.ProviderFactory import ProviderFactory

app = FastAPI()

@app.get('/providers')
async def get_providers():
    providers = ProviderFactory.read_providers()
    providers_dict = []
    for p in providers:
        providers_dict.append(p.to_dict())
    return jsonable_encoder(providers_dict)


@app.get('/services')
async def get_cpsv_services():
    providers = ProviderFactory.read_providers()
    merged = []
    for provider in providers:
        services = provider.get_services()
        if services is not None:
            merged += services
    return merged


@app.get('/services/{id}')
async def get_cpsv_service_details(id: str):
    output = []
    providers = ProviderFactory.read_providers()
    for provider in providers:
        p_output = provider.get_service_details(id)
        if p_output is not None:
            output.append({"provider": provider.name, "results": p_output})
    if len(output) == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return output


@app.get('/outputs')
async def get_cpsv_outputs():
    providers = ProviderFactory.read_providers()
    merged = []
    for provider in providers:
        outputs = provider.get_outputs()
        if outputs is not None:
            merged += outputs
    return merged
