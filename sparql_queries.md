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
> returns all data directly connected
not properly formatted

    PREFIX cpsv:<http://purl.org/vocab/cpsv#>
    PREFIX dct:<http://purl.org/dc/terms/>
    
    SELECT ?name ?verb ?object
    WHERE {?id a cpsv:PublicService.
        ?id dct:title ?name.
        ?id ?verb ?object.
        FILTER (regex(str(?id),"PLACE_ID_HERE"))
    }
         

# Vocabulary

1. - [ ] Address
2. - [ ] Agent 
3. - [ ] Business Event
4. - [ ] Channel
5. - [ ] Collection
6. - [ ] Concept
7. - [ ] Concession Contract
8. - [ ] Contact Point
9. - [ ] Cost
10. - [ ] Dataset
11. - [ ] Event
12. - [ ] Evidence 
13. - [ ] Evidence Type 
14. - [ ] Legal Resource 
15. - [ ] Life Event 
16. - [ ] Organization 
17. - [ ] Output 
18. - [ ] Participation 
19. - [ ] Public Organization 
20. - [ ] Public Service 
21. - [ ] Requirement
22. - [ ] Rule 
23. - [ ] Service Concession Contract 
24. - [ ] Temporal Entity 
        

## Public Service
1. - [x] addressee: _Code_
2. - [x] contact point: _Contact Point_
    1. - [ ] availability restriction: _Temporal Entity_
        1. - [ ] description: _Text_
        2. - [ ] frequency: _Code_
    2. - [ ] contact page: _Document_
    3. - [ ] has email: _Literal_
    4. - [ ] has telephone: _Literal_
    5. - [ ] opening hours: _Temporal Entity_
        1. - [ ] description: _Text_
        2. - [ ] frequency: _Code_
3. - [x] description: _Text_
4. follows: _Rule_
    1. - [ ] description: _Text_
    2. - [ ] identifier: _Literal_
    3. - [ ] implements: _Legal Resource_
    4. - [ ] language: _LinguisticSystem_
    5. - [ ] name: _Text_
    6. - [ ] type: _Code_
5. - [x] functions of government: _Code_
6. - [x] has channel: _Channel_
    1. - [ ] availability restriction: _Temporal Entity_
        1. - [ ] description: _Text_
        2. - [ ] frequency: _Code_
    2. - [ ] description: _Text_   
    3. - [ ] has input: _Evidence_
        1. - [ ] description: _Text_
        2. - [ ] identifier: _Literal_
        3. - [ ] is conformant to: _Evidence Type_
            1. - [ ] evidence type classification: _Code_
            2. - [ ] identifier: _Literal_
        4. - [ ] language: _LinguisticSystem_
        5. - [ ] name: _Text_
        6. - [ ] related documentation: _Document_
        7. - [ ] supports requirement: _**Requirement**_
        8. - [ ] type: _Code_
    4. - [ ] identifier: _Literal_   
    5. - [ ] opening hours: _Temporal Entity_
        1. - [ ] description: _Text_
        2. - [ ] frequency: _Code_
    6. - [ ] owned by: _Organization_   
    7. - [ ] processing time: _Duration_   
    8. - [ ] type: _Code_   
7. - [x] has competent authority: _Public Organization_
     1. - [ ] preferred label: _Text_
     2. - [ ] spatial: _AdministrativeTerritorialUnit_
8. - [x] has cost: _Cost_
     1. - [x] currency: _Code_
     2. - [x] description: _Text_
     3. - [x] has value: _Double_
     4. - [x] if accessed through: _**Channel**_
     5. - [x] is defined by: _**Organization**_
9. - [x] has input: _Evidence_
      1. - [x] description: _Text_
      2. - [x] identifier: _Literal_
      3. - [x] is conformant to: _Evidence Type_
          1. - [ ] evidence type classification: _Code_
          2. - [ ] identifier: _Literal_
      4. - [x] language: _LinguisticSystem_
      5. - [x] name: _Text_
      6. - [x] related documentation: _Document_
      7. - [x] supports requirement: _**Requirement**_
      8. - [x] type: _Code_
10. - [x] has input type: _Evidence Type_
    1. - [ ] evidence type classification: _Code_
    2. - [ ] identifier: _Literal_
11. - [x] has legal resource: _Legal Resource_
    1. - [ ] related: _**Legal_Resource**_ 
12. - [x] has participation: _Participation_
    1. - [ ] description: _Text_
    2. - [ ] has participant: _Agent_
        1. - [ ] address: _Address_
            1. - [ ] address area: _Text_
            2. - [ ] address ID: _Literal_
            3. - [ ] administrative unit level 1: _Text_
            4. - [ ] administrative unit level 2: _Text_
            5. - [ ] full address: _Text_
            6. - [ ] local designator: _Literal_
            7. - [ ] locator name: _Text_
            8. - [ ] post code: _Literal_
            9. - [ ] post name: _Text_
            10. - [ ] post office box: _Literal_
            11. - [ ] thoroughfare: _Text_
        2. - [ ] identifier: _Literal_
        3. - [ ] name: _Text_
        4. - [ ] participates: _Participation_
            1. - [ ] description: _Text_
            2. - [ ] has participant: _**Agent**_
            3. - [ ] identifier: _Literal_
            4. - [ ] role: _Code_
    3. - [ ] identifier: _Literal_
    4. - [ ] role: _Code_
13. - [x] holds requirement: _Requirement_
    1. - [ ] fulfils: _Rule_
    2. - [ ] has supporting evidence: _**Evidence**_
    3. - [ ] identifier: _Literal_
    4. - [ ] name: _Text_
    5. - [ ] type: _Code_
14. - [x] identifier: _Literal_
15. - [x] is classified by: _Concept_
16. - [x] is described at: _Dataset_
    1. - [ ] description: _Text_
    2. - [ ] has part: _**Public Service**_
    3. - [ ] identifier: _Literal_
    4. - [ ] landing page: _Document_
    5. - [ ] publisher: _**Agent**_
    6. - [ ] title: _Text_
17. - [x] is grouped by: _Event_
    1. - [x] description: _Text_
    2. - [x] has related service: _**Public Service**_
    3. - [x] identifier: _Literal_
    4. - [x] name: _Text_
    5. - [x] type: _Code_
18. - [x] keyword: _Text_
19. - [x] language: _LinguisticSystem_
20. - [x] name: _Text_
21. - [x] processing time: _Duration_
22. - [x] produces: _Output_
    1. - [x] description: _Text_
    2. - [x] identifier: _Literal_
    3. - [x] language: _LinguisticSystem_
    4. - [x] name: _Text_
    5. - [x] type: _Code_
23. - [x] related service: _**Public Service**_
24. - [x] requires: _**Public Service**_
25. - [x] sector: _Code_
26. - [x] spatial: _Location_
27. - [x] status: _Code_
28. - [x] thematic area: _Code_