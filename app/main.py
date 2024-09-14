import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from .providers.ProviderFactory import ProviderFactory

app = FastAPI()
providers = ProviderFactory.read_providers()

@app.get('/providers')
async def get_providers():
    providers_dict = []
    for p in providers:
        providers_dict.append(p.to_dict())
    return jsonable_encoder(providers_dict)


@app.get('/services')
async def get_cpsv_services():
    merged = []
    for provider in providers:
        services = provider.get_services()
        if services is not None:
            merged += services
    return merged


@app.get('/services/{id}')
async def get_cpsv_service_details(id: str):
    merged = []
    for provider in providers:
        p_output = provider.get_service_details(id)
        if p_output is not None:
            merged.append({"provider": provider.name, "results": p_output})
    if len(merged) == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return merged

@app.get('/organizations')
async def get_cpsv_organizations():
    merged = []
    for provider in providers:
        organizations = provider.get_organizations()
        if organizations is not None:
            merged += organizations
    return merged

@app.get('/evidences')
async def get_cpsv_evidences():
    merged = []
    for provider in providers:
        evidences = provider.get_evidences()
        if evidences is not None:
            merged += evidences
    return merged

@app.get('/requirements')
async def get_cpsv_requirements():
    merged = []
    for provider in providers:
        requirements = provider.get_requirements()
        if requirements is not None:
            merged += requirements
    return merged

@app.get('/rules')
async def get_cpsv_requirements():
    merged = []
    for provider in providers:
        rules = provider.get_rules()
        if rules is not None:
            merged += rules
    return merged

@app.get('/legalResources')
async def get_cpsv_legal_resources():
    merged = []
    for provider in providers:
        legal_resources = provider.get_legal_resources()
        if legal_resources is not None:
            merged += legal_resources
    return merged


@app.get('/outputs')
async def get_cpsv_outputs():
    merged = []
    for provider in providers:
        outputs = provider.get_outputs()
        if outputs is not None:
            merged += outputs
    return merged
