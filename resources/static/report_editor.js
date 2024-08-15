(async () => {
    const reportIDInput = document.getElementById("report-id");
    const reportTitleInput = document.getElementById("report-title");
    const reportConclusionInput = document.getElementById("report-conclusion");
    const reportFormSubmitBtn = document.getElementById("report-form-submit-btn");
    const reportFindingElements = document.getElementsByClassName("report-finding");

    const genAiDescBtns = document.getElementsByClassName("gen-ai-desc");
    const genAiRecBtns = document.getElementsByClassName("gen-ai-rec");

    Array.from(genAiDescBtns).forEach(descBtn => {
        descBtn.addEventListener("click", async ev => {
            if(!ev.target.value) return;
            const resp = await fetch( `/api/findings/${ev.target.value}/generate-description-automatically`,{
                method: "PUT",
            });
            if(resp.ok) {
                const updatedFinding = await resp.json();
                const el = document.getElementById(`description-${ev.target.value}`)
                if(el) el.value = updatedFinding.description;
            }
        });
    })
    Array.from(genAiRecBtns).forEach(recBtn => {
        recBtn.addEventListener("click", async ev => {
            if(!ev.target.value) return;
            const resp = await fetch( `/api/findings/${ev.target.value}/generate-recommendation-automatically`,{
                method: "PUT",
            });
            if(resp.ok) {
                const updatedFinding = await resp.json();
                const el = document.getElementById(`recommendation-${ev.target.value}`)
                if(el) el.value = updatedFinding.description;
            }
        });
    })

    reportFormSubmitBtn.addEventListener("click", async ev => {
        ev.preventDefault();
        const reportFindings = Array.from(reportFindingElements).map(finding => {
            const id = finding.getElementsByClassName("id").item(0).value;
            const description = finding.getElementsByClassName("description").item(0).value;
            const recommendation = finding.getElementsByClassName("recommendation").item(0).value;
            return { id, description, recommendation }
        });

        // STEP 1: Update the report
        const res = await fetch(`/api/reports/${reportIDInput.value}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                title: reportTitleInput.value,
                conclusion: reportConclusionInput.value,
            })
        })
        if(!res.ok) {
            alert(`Failed to update finding with id ${finding.id}`) 
            return;
        }

        // STEP 2: Update all findings
        for(const finding of reportFindings) {
            const data = { recommendation: finding.recommendation, description: finding.description, }
            const resp = await fetch( `/api/findings/${finding.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data)
            });
            if(!resp.ok) { 
                alert(`Failed to update finding with id ${finding.id}`) 
                return;
            }
        }
    });
})();
