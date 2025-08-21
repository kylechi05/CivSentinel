"use server";

import {
    getCrimes,
    getLocationMapping,
    getPredictedCrimes,
} from "@/utils/supabase";
import { CrimeMapWrapper } from "@/components/CrimeMapWrapper";
import { CrimeType } from "@/types/Crimes";

export default async function Home() {
    const crimes = await getCrimes();
    const predictedCrimes = await getPredictedCrimes();
    const locationMapping = await getLocationMapping();

    if (crimes.status !== 200 || locationMapping.status !== 200) {
        return (
            <div>
                Crime Data is currently not available, please try again later.
            </div>
        );
    }

    if (predictedCrimes.status !== 200) {
        predictedCrimes.data = [];
    }

    const mapping = locationMapping.data ?? {};

    const crimeData: CrimeType[] =
        crimes.data?.map((crime) => ({
            ...crime,
            date_reported: new Date(crime["date_reported"]).toLocaleString(),
            date_time_occurred: new Date(
                crime["date_time_occurred"],
            ).toLocaleString(),
            lat: mapping[crime["general_location"]]["lat"],
            lon: mapping[crime["general_location"]]["lon"],
        })) ?? [];


    return (
        <div className="h-full">
            <main className="row-start-2 flex h-full flex-col items-center gap-[32px] sm:items-start">
                <CrimeMapWrapper crimeData={crimeData} />
            </main>
        </div>
    );
}
