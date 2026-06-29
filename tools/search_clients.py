from services.supabase_service import get_supabase


def search_clients(search: str):
    supabase = get_supabase()

    identities = (
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

    results = []

    for identity in identities:
        client = (
            supabase
            .table("clients")
            .select("display_code")
            .eq("id", identity["client_id"])
            .single()
            .execute()
            .data
        )

        results.append({
            "client_id": identity["client_id"],
            "display_code": client["display_code"],
            "first_name": identity["first_name"],
            "last_name": identity["last_name"],
            "email": identity["email"],
        })

    return results
