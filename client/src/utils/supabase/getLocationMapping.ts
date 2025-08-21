import getClient from "./getClient";

export default async function getLocationMapping() {
    const supabase = getClient();

    try {
        const { data, error } = await supabase.rpc("get_location_mapping");

        if (error) {
            throw new Error(error.message);
        }

        const mapping: {
            [key: string]: {
                general_location: string;
                lon: number;
                lat: number;
                city: string;
                state: string;
                street_address: string;
                zip_code: string;
            };
        } = {};

        data.forEach(
            (map: {
                general_location: string;
                lon: number;
                lat: number;
                city: string;
                state: string;
                street_address: string;
                zip_code: string;
            }) => {
                mapping[map["general_location"]] = { ...map };
            },
        );

        return {
            status: 200,
            data: mapping,
        };
    } catch (error) {
        return {
            status: 500,
            message: `Internal error fetching crime data: ${error}`,
        };
    }
}
