# Sparql Queries

## 1. Services

### 1.1 Basic list of services

    PREFIX cpsv:<http://purl.org/vocab/cpsv#>
    PREFIX dct: <http://purl.org/dc/terms/>

    SELECT DISTINCT ?id ?name
    WHERE {
        ?id a cpsv:PublicService.
        ?id dct:title ?name
    } 
    ORDER BY ?name

## 1.2 Search service
> returns all data directly connected, not properly formatted

    PREFIX cpsv:<http://purl.org/vocab/cpsv#>
    PREFIX dct:<http://purl.org/dc/terms/>
    
    SELECT ?name ?verb ?object
    WHERE {?id a cpsv:PublicService.
        ?id dct:title ?name.
        ?id ?verb ?object.
        FILTER (regex(str(?id),"PLACE_ID_HERE"))
    }