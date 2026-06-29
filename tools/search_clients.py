from services.supabase_service import get_supabase

def search_clients(search: str):
    supabase = get_supabase()

    return (
        supabase
        .table("client_identities")
        .select("client_id, first_name, last_name, email")
        .or_(
            f"first_name.ilike.%{search}%,"
            f"last_name.ilike.%{search}%,"
            f"email.ilike.%{search}%"
        )
        .limit(10)
        .execute()
        .data
    )
