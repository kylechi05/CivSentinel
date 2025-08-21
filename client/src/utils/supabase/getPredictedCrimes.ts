import getClient from "./getClient";

export default async function getPredictedCrimes() {
    const supabase = getClient();

    const crimes = [];
    const pageSize = 1000;

    let from = 0;
    let to = pageSize - 1;

    try {
        while (from === crimes.length) {
            const { data, error } = await supabase
                .from("predicted_crimes")
                .select("*")
                .range(from, to);

            if (error) {
                throw new Error(error.message);
            }

            crimes.push(...data)

            from += pageSize;
            to += pageSize;
        }

        return {
            status: 200,
            data: crimes
        }
    } catch (error) {
        return {
            status: 500,
            message: `Internal error fetching crime data: ${error}`,
        };
    }
}
