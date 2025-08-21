"use client";
import { useState } from "react";

export function DisclaimerModal() {
    const [acknowledged, setAcknowledged] = useState(false);
    const [showDisclaimerModal, setDisclaimerModal] = useState(true);
    return (
        showDisclaimerModal && (
            <div className="absolute inset-x-0 top-16 bottom-0 z-10 bg-neutral-700/50 backdrop-blur-md">
                <div className="mx-24 my-18 flex flex-col items-center justify-center gap-5 rounded-3xl bg-white px-12 py-6 text-start">
                    <h1 className="flex flex-col text-lg font-medium">
                        Welcome to CivSentinel
                    </h1>
                    <h2 className="font-medium text-neutral-700">Disclaimer</h2>
                    <div className="space-y-3 text-neutral-700">
                        <p>
                            Each location marker on the crime map corresponds to
                            a rough geographical estimate of a reported incident
                            taken from the University of Iowa&apos;s Crime Log
                            and historical records provided by University Campus
                            Safety. It does not imply guilt, nor does it
                            indicate that any specific address is directly
                            associated with an incident.
                        </p>
                        <p>
                            CivSentinel does not explicitly or implicitly
                            guarantee the accuracy, completeness, or timeliness
                            of the information presented. Data may change or be
                            updated at any time without notice.
                        </p>
                        <p>
                            CivSentinel and its developers assume no liability
                            for any loss, cost, damage, or expense arising
                            directly or indirectly from use of the site. In no
                            event shall CivSentinel or its developers be liable
                            for consequential damages or for direct damages
                            resulting from reliance on the information
                            displayed, including but not limited to the crime
                            map and prediction map. Use of this site and its
                            information is solely at the viewer&apos;s own risk.
                        </p>
                    </div>
                    <div className="flex flex-col items-center justify-center gap-2">
                        <label className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                checked={acknowledged}
                                onChange={(e) =>
                                    setAcknowledged(e.target.checked)
                                }
                                className="cursor-pointer"
                            />
                            I Acknowledge
                        </label>

                        <button
                            type="button"
                            className={`rounded-2xl px-4 py-2 ${
                                acknowledged
                                    ? "bg-blue-600 text-white hover:bg-blue-700"
                                    : "cursor-not-allowed bg-gray-300 text-gray-500"
                            }`}
                            disabled={!acknowledged}
                            onClick={() => setDisclaimerModal(false)}
                        >
                            Submit
                        </button>
                    </div>
                </div>
            </div>
        )
    );
}
