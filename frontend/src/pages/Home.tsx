import Navbar from "../components/Navbar";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import  { SERVER_BASE_URL } from "../libs/config.ts";
import { GetAuditReport } from "../libs/dto.ts";

export default function Home() {
    const navigate = useNavigate();
    const [ address, setAddress ] = useState("");
    const onSubmitButtonClicked = async () => {
        console.log(address);
        const resp = await fetch(`${SERVER_BASE_URL}/api/audit`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                title: "An Audit Report",
                address,
            })
        });
        if(resp.ok) {
            const report = (await resp.json()) as GetAuditReport;
            return navigate(`/audit-report/${report.id}`);
        }
    }

    return (
        <div>
            <Navbar/>
            <section className="bg-white dark:bg-gray-900">
                <div className="py-8 px-4 mx-auto max-w-screen-xl text-center lg:py-16">
                    <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl dark:text-white">Start Auditing Your Smart Contract Application Now!</h1>
                    <p className="mb-8 text-lg font-normal text-gray-500 lg:text-xl sm:px-16 lg:px-48 dark:text-gray-400">Gunther is a free and open source software for creating audit report for smart contract based on Slither and other analyzer in the future.</p>
                    <div className="flex flex-col space-y-4 sm:flex-row sm:justify-center sm:space-y-0 sm:space-x-4">
                        <div className="sm:max-w-sm w-full">
                            <input type="text" onChange={e => setAddress(e.target.value) } id="etherscan-address-input" placeholder="Etherscan Address" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"/>
                        </div>
                        <button onClick={onSubmitButtonClicked} className="inline-flex justify-center items-center py-3 px-5 text-base font-medium text-center text-white rounded-lg bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-900">
                            Try Audit
                            <svg className="w-3.5 h-3.5 ms-2 rtl:rotate-180" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                                <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </section>
        </div>
    )
}
