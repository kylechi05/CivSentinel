import { Dispatch, SetStateAction } from "react";

export default function NavBar({
    setMapType,
}: {
    setMapType: Dispatch<SetStateAction<"live" | "predicted">>;
}) {
    return (
        <div className="flex h-16 flex-row items-center gap-16 px-8 bg-[#e9f0ef]">
            <h1 className="text-xl font-medium">CivSentinel</h1>
            <div className="flex flex-row gap-10">
                <button
                    className="cursor-pointer hover:font-medium"
                    onClick={() => setMapType("live")}
                >
                    <h2>Live Crime Map</h2>
                </button>
                <button
                    className="cursor-pointer hover:font-medium"
                    onClick={() => setMapType("predicted")}
                >
                    <h2>Crime Forcaster</h2>
                </button>
            </div>
        </div>
    );
}
