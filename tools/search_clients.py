def search_clients(search: str):
    supabase = get_supabase()

    return (
        supabase
        .table("clients")
        .select("id, display_code")
        .ilike("display_code", f"%{search}%")
        .limit(10)
        .execute()
        .data
    )
