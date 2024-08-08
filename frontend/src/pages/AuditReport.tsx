import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { useParams } from "react-router-dom";
import { DetailedAuditReport } from "../libs/dto";
import  { SERVER_BASE_URL } from "../libs/config.ts";


export default function Audit() {
    const { id } =  useParams();
    const [ report, setReport ] = useState<DetailedAuditReport>({
        findings: [],
    });
    useEffect(() => {
        (async () => {
            const resp = await fetch(`${SERVER_BASE_URL}/api/reports/${id}`);
            if(resp.ok) {
                setReport(await resp.json() as DetailedAuditReport);
            }
        })();
    }, []);
    return (
        <div className="dark:bg-gray-900 pb-5">
            <Navbar/>
            <div className="px-5">
                <div className="mb-6">
                    <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Title</label>
                    <input type="email" id="email" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Audit report title here" value={report.title} onChange={ev => setReport({ ...report, title: ev.target.value })} required />
                </div>
                { ...report.findings.map(finding => (
                    <div>
                    </div>
                )) }
                <div className="mb-6">
                    <label htmlFor="message" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Conclusions</label>
                    <textarea id="message" rows={4} className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Write your thoughts here..." onChange={ev => setReport({ ...report, conclusion: ev.target.value }) }>{report.conclusion}</textarea>
                </div> 
            </div>
        </div>
    )
}
