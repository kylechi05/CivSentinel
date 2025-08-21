import { createClient } from "@supabase/supabase-js";

export default function getClient() {
    const supabaseURL = process.env.SUPABASE_URL ?? "";
    const supabaseKey = process.env.SUPABASE_KEY ?? "";

    const supabase = createClient(supabaseURL, supabaseKey);
    return supabase;
}
