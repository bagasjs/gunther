

export interface GetAuditFinding {
    id: number
    title: string
    severity: string
    raw: string
    description: string | null
    recommendation: string | null
    report_id: number | null
    created: string | null
    updated: string | null
}

export interface GetAuditReport {
    id: number
    title: string
    address: string
    conclusion: string
    created: string
    updated: string
}

export interface DetailedAuditReport {
    id: number
    title: string
    address: string
    conclusion: string
    created: string
    updated: string
    findings: GetAuditFinding[]
}
