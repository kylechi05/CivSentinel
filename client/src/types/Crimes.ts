export interface CrimeType {
    id: number;
    created_at: string;
    associated_id: string;
    date_reported: string;
    date_time_occurred: string;
    general_location: string;
    natures_of_crime: string;
    lat: number;
    lon: number;
}

export interface PredictedCrimeType{
    id: number;
}