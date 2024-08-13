# TODO

## REFERENCES
- FastAPI MVC: https://github.com/ViktorViskov/fastapi-mvc/tree/main

## FUTURE
- Refactor into web application architecture
- Add a way to parameterize the smart contract network
- Authentication/Authorization for external user

### Create REST-api for client side report generation
- Find out whether FastAPI would be a viable option of Flask, since async would make the audit process faster
- The REST-api should have the following 
    - Auditor endpoint
        - /auditor/audit -> This will need address as an input, then we do all the audit flow if required
    - Reports endpoint
        - [GET] /reports -> This will return the id,address,title of all reports (maybe pagination?)
        - [GET] /reports/{id} -> This will return all the information related to the report including it's findings
        - [GET or POST (TENTATIVE)] /reports/{id}/generate-conclusion/{writer:[gemini|chatgpt]}
    - Findings endpoint
        - [GET] /findings -> This will return the id,title,report_id of all findings
        - [GET] /findings/{id} -> This will return all the information related to findings
        - [GET or POST (TENTATIVE)] /findings/{id}/generate-better-title/{writer:[gemini|chatgpt]}
        - [GET or POST (TENTATIVE)] /findings/{id}/generate-description/{writer:[gemini|chatgpt]}
        - [GET or POST (TENTATIVE)] /findings/{id}/generate-recommendation/{writer:[gemini|chatgpt]}
- Create a better Web UI for client where there's an editor for the report
- If the REST-api is actually good the CLI should just use the REST-api

## DONE

- Store the audit result and re-audit every weeks
- Recommendation
- Timestamp
