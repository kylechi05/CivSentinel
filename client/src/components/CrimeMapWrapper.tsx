"use client";

import { useState } from "react";
import dynamic from "next/dynamic";

import NavBar from "./NavBar";
import { CrimeType } from "@/types/Crimes";
import { DisclaimerModal } from "./DisclaimerModal";

const CrimeMap = dynamic(
    () => import("./CrimeMap").then((mod) => mod.CrimeMap),
    {
        ssr: false,
    },
);

export function CrimeMapWrapper({ crimeData }: { crimeData: CrimeType[] }) {

    const [mapType, setMapType] = useState<"live" | "predicted">("live");

    return (
        <div className="relative size-full">
            <NavBar setMapType={setMapType} />
            <DisclaimerModal />
            <div className="relative z-0">
                {mapType === "live" ? (
                    <CrimeMap crimeData={crimeData} />
                ) : (
                    <div>In Progress</div>
                )}
            </div>
        </div>
    );
}
