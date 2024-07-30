# TODO

## FUTURE
- Add a way to parameterize the smart contract network

### Create REST-api for client side report generation
- Find out whether FastAPI would be a viable option of Flask, since async would make the audit process faster
- The REST-api should have the following 
    - Auditor endpoint
        - /auditor/audit -> This will need address as an input, then we do all the audit flow if required
    - Reports endpoint
        - [GET] /reports -> This will return the id,address,title of all reports (maybe pagination?)
        - [GET] /reports/{id} -> This will return all the information related to the report including it's findings
        - [(TENTATIVE)] /reports/{id}/generate-conclusion/{writer:[gemini|chatgpt]}
    - Findings endpoint
        - [GET] /findings -> This will return the id,title,report_id of all findings
        - [GET] /findings/{id} -> This will return all the information related to findings
        - [(TENTATIVE)] /findings/{id}/generate-better-title/{writer:[gemini|chatgpt]}
        - [(TENTATIVE)] /findings/{id}/generate-description/{writer:[gemini|chatgpt]}
        - [(TENTATIVE)] /findings/{id}/generate-recommendation/{writer:[gemini|chatgpt]}

## DONE

- Store the audit result and re-audit every weeks
- Recommendation
- Timestamp
