import { useRouteError } from "react-router-dom";

export default function Error() {
    const error = useRouteError();
    return (
        <div className="p-5 flex items-center w-full h-screen justify-center">
            <h1 className="text-5xl font-bold mb-3">
                {/* @ts-ignore */}
                { error.status } { error.statusText || error.message }
            </h1>
        </div>
    )
}
