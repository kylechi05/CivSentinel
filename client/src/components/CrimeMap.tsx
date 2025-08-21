"use client";

import "leaflet/dist/leaflet.css";

import { useState, useMemo } from "react";
import L from "leaflet";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { MapMarkerIcon } from "./icons/MapMarkerIcon";
import { CrimeType } from "@/types/Crimes";
import { renderToStaticMarkup } from "react-dom/server";

const markerHtml = renderToStaticMarkup(
    <div style={{ position: "relative", width: 24, height: 24 }}>
        <div
            style={{
                position: "absolute",
                bottom: -1.5,
                left: "50%",
                transform: "translateX(-50%)",
                width: "18px",
                height: "10px",
                background: "rgba(0,0,0,0.15)",
                borderRadius: "50%",
                filter: "blur(2px)",
            }}
        />
        <MapMarkerIcon />
    </div>,
);

export function CrimeMap({ crimeData }: { crimeData: CrimeType[] }) {
    const [dateWindow, setDateWindow] = useState({
        from: new Date(new Date().setMonth(new Date().getMonth() - 6)),
        to: new Date(),
    });

    const [dateError, setDateError] = useState(false);

    const lats = crimeData.map((crime) => crime.lat);
    const lons = crimeData.map((crime) => crime.lon);

    const centerLat = (Math.min(...lats) + Math.max(...lats)) / 2;
    const centerLon = (Math.min(...lons) + Math.max(...lons)) / 2;

    const mapCenter: [number, number] = [centerLat, centerLon];

    const filteredCrimeData = useMemo(
        () =>
            crimeData.filter((crime) => {
                const crimeDate = new Date(crime.date_reported);
                return crimeDate >= dateWindow.from && crimeDate <= dateWindow.to;
            }),
        [crimeData, dateWindow],
    );

    const handleFromDateChange = (fromDate: Date) => {
        if (validateDates(fromDate, dateWindow.to)) {
            setDateWindow((prev) => ({ ...prev, from: fromDate }));
        }
    };

    const handleToDateChange = (toDate: Date) => {
        if (validateDates(dateWindow.from, toDate)) {
            setDateWindow((prev) => ({ ...prev, to: toDate }));
        }
    };

    const validateDates = (fromDate: Date, toDate: Date) => {
        setDateError(fromDate > toDate);
        return fromDate <= toDate;
    };

    return (
        <div className="relative h-[calc(100vh-4rem)] w-full">
            <div className="absolute border-1 border-gray-200 top-32 left-3 z-10 flex w-64 flex-col gap-2 rounded-2xl bg-white px-4 py-2 shadow-sm">
                <h1 className="text-lg font-medium">Filters</h1>
                <div className="grid grid-cols-3 gap-x-2">
                    <span>From: </span>
                    <input
                        name="from"
                        id="from"
                        type="date"
                        className="col-span-2 cursor-pointer focus:border-b-[1.5px] focus:bg-neutral-100 focus:outline-none"
                        value={dateWindow.from.toISOString().split("T")[0]}
                        onChange={(e) =>
                            handleFromDateChange(new Date(e.target.value))
                        }
                    />
                    <span>To:</span>
                    <input
                        name="to"
                        id="to"
                        type="date"
                        className="col-span-2 cursor-pointer focus:border-b-[1.5px] focus:bg-neutral-100 focus:outline-none"
                        value={dateWindow.to.toISOString().split("T")[0]}
                        onChange={(e) =>
                            handleToDateChange(new Date(e.target.value))
                        }
                    />
                </div>
                {dateError && (
                    <div className="text-sm text-red-400">
                        From Date must be earlier than To Date
                    </div>
                )}
            </div>
            <MapContainer
                center={mapCenter}
                zoom={12}
                className="z-0 size-full"
            >
                <TileLayer
                    url="https://cartodb-basemaps-a.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://www.carto.com/">CARTO</a>'
                    subdomains={["a", "b", "c", "d"]}
                />

                {filteredCrimeData.map((crime) => (
                    <Marker
                        key={crime.id}
                        position={[crime.lat, crime.lon]}
                        icon={L.divIcon({
                            html: markerHtml,
                            className: "",
                            iconSize: [24, 24],
                        })}
                    >
                        <Popup>
                            <strong>{crime.natures_of_crime}</strong>
                            <br />
                            {crime.general_location}
                            <br />
                            Reported:{" "}
                            {new Date(crime.date_reported).toLocaleDateString()}
                        </Popup>
                    </Marker>
                ))}
            </MapContainer>
        </div>
    );
}
