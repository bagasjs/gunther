import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { useParams } from "react-router-dom";
import { DetailedAuditReport, GetAuditFinding, UpdateAuditFinding, UpdateAuditReport } from "../libs/dto";
import  { SERVER_BASE_URL } from "../libs/config.ts";

export default function AuditReport() {
    const { id } =  useParams();
    /** @ts-ignore **/
    const [ report, setReport ] = useState<DetailedAuditReport>({
        findings: [ ],
    });

    useEffect(() => {
        (async () => {
            const resp = await fetch(`${SERVER_BASE_URL}/api/reports/${id}`);
            if(resp.ok) {
                setReport(await resp.json() as DetailedAuditReport);
            }
        })();
    }, []);

    const setAuditReportFinding = (findingId: number, newfinding: GetAuditFinding) => {
        setReport(prevReport => ({
            ...prevReport,
            findings: prevReport.findings.map(finding => finding.id === findingId ? newfinding : finding)
        }))
    }

    const generateDescriptionAutomaticaly = async (findingId: number) => {
        const resp = await fetch(`${SERVER_BASE_URL}/api/findings/${findingId}/generate-description-automatically`,{
            method: "PUT",
        });
        if(resp.ok) {
            const updatedFinding = await resp.json() as GetAuditFinding;
            setAuditReportFinding(findingId, updatedFinding);
        }
    }

    const generateRecommendationAutomatically = async (findingId: number) => {
        const resp = await fetch(
            `${SERVER_BASE_URL}/api/findings/${findingId}/generate-recommendation-automatically`,{
            method: "PUT",
        });
        if(resp.ok) {
            const updatedFinding = await resp.json() as GetAuditFinding;
            setAuditReportFinding(findingId, updatedFinding);
        }
    }

    const updateAuditReport = async () => {
        // STEP 1: Update with UpdateAuditReport DTO
        const data: UpdateAuditReport = {
            title: report.title,
            conclusion: report.conclusion,
        }
        const resp = await fetch(
            `${SERVER_BASE_URL}/api/reports/${report.id}`,{
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data)
            });
            if(!resp.ok) { 
                alert("Failed to update report") 
                return
            }
        // STEP 2: Update every finding with UpdateAuditFinding DTO
        for(const finding of report.findings) {
            const data: UpdateAuditFinding = {
                description: finding.description ?? "",
                recommendation: finding.recommendation ?? "",
            }
            const resp = await fetch(
                `${SERVER_BASE_URL}/api/findings/${finding.id}`,{
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

    }

    return (
        <div className="dark:bg-gray-900 pb-5">
            <Navbar/>
            <div className="px-5">
                <div className="mb-6">
                    <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Title</label>
                    <input type="email" id="email" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Audit report title here" value={report.title} onChange={ev => setReport({ ...report, title: ev.target.value })} required />
                </div>
                <h2 className="mb-2 text-2xl font-bold text-gray-900 dark:text-white">Findings</h2>
                <div className="pl-5">
                { ...report.findings.map(finding => (
                        <div>
                            <h3 className="mb-2 text-lg font-medium text-gray-900 dark:text-white">{finding.title}</h3>
                            <div className="mb-6">
                                <label htmlFor="message" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Description</label>
                                <textarea id="message" rows={4} className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Write your thoughts here..." value={finding.description ?? ""} onChange={ev => setAuditReportFinding(finding.id, { ...finding, description: ev.target.value })}></textarea>
                                <div className="mt-3">
                                    <button type="button" className="text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" onClick={() => generateDescriptionAutomaticaly(finding.id)}>Paraphrase with AI</button>
                                </div>
                            </div> 
                            <div className="mb-6">
                                <label htmlFor="message" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Recommendation</label>
                                <textarea id="message" rows={4} className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Write your thoughts here..." value={finding.recommendation ?? ""} onChange={ev => setAuditReportFinding(finding.id, { ...finding, recommendation: ev.target.value })}></textarea>
                                <div className="mt-3">
                                    <button type="button" className="text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" onClick={() => generateRecommendationAutomatically(finding.id) }>Paraphrase with AI</button>
                                </div>
                            </div> 
                        </div>
                )) }
                </div>
                <div className="mb-6">
                    <label htmlFor="message" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Conclusions</label>
                    <textarea id="message" rows={4} className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Write your thoughts here..." onChange={ev => setReport({ ...report, conclusion: ev.target.value }) } value={report.conclusion}></textarea>
                </div> 
                <div className="w-full flex justify-end">
                    <button onClick={updateAuditReport}type="button" className="text-white bg-green-700 hover:bg-green-800 focus:outline-none focus:ring-4 focus:ring-green-300 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800">Save</button> 
                </div>
            </div>
        </div>
    )
}
