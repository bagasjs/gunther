import { createBrowserRouter } from "react-router-dom";
import Home from "./pages/Home";
import Error from "./pages/Error";
import AuditReport from "./pages/AuditReport";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Home/>,
        errorElement: <Error/>
    },
    {
        path: "/audit-report/:id",
        element: <AuditReport/>,
        errorElement: <Error/>
    },
]);
