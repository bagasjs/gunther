import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { useParams } from "react-router-dom";
import { DetailedAuditReport } from "../libs/dto";


export default function Audit() {
    const { id } =  useParams();
    const [ report, setReport ] = useState<DetailedAuditReport|null>(null);
    useEffect(() => {
        (async () => {
        })();
    }, []);
    return (
        <div>
            <Navbar/>
            <p>{id}</p>
        </div>
    )
}
