# bodytrak-precursor-code

# Stack Used
| BodyTrak       |   Implemented  |
|--------------- |----------------|
|Django          | Yes            | 
|Rest            | Yes            |
|pytest          | Yes            |
|Docker          | Yes            |
|Linux           | Yes[In VM]     |
|Redis           | Yes,Provisioned|
|Email           | Yes,Provisioned|
|PostGreSQL      | No,MySQL       |
|BitBucket       | No,GitHub      |     
|Sentry          | No,BuiltIn Log |
|Celery          | No,Due to OS   |
|GitHub Pipeline | No             |     
|Grafana         | No             |
|Snyk            | No             |
|AirFlow         | No             |
|GraphQL         | No             |
|CodeCov         | No,Coderabbit  |
|Azure           | No             |

# Additional Tools
- DJANGO DEBUG TOOLBAR for easy inspection
- DJOSER for Auth JWT
- Silk for DB performance measurement(Removed from codebase)
- Bakery for Mock Tests
- Locust for Performance measurement
  ![locust](https://github.com/user-attachments/assets/eee4a681-92a6-4e92-ad12-29ba4174fa4a)
- Observation - 150 concurrent users is the limit , mainly due to Dev storage server capacity

## Mockeroo for DB data generation
![image](https://github.com/user-attachments/assets/8c947134-82ab-4e81-aebd-7c3c575506d6)

## Possible Extensions if time permitted
- More Unit Test(Complete workflow), Integration Tests, Running Static,Security Code Analysis & Implement
- Implement Caching , Logging , Worker Threads (Celery) 
- Functionality wise - Implemented Promotions/Offers,Added images for products, Send Email once order created via custom signals
- CI/CD, Deployment 

