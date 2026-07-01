from services.supabase_service import get_supabase


def search_clients(search: str):
    supabase = get_supabase()
    search = search.strip()

    clients = (
        supabase
        .table("clients")
        .select("id, display_code, programme, status")
        .ilike("display_code", f"%{search}%")
        .limit(20)
        .execute()
        .data
    )

    results = []

    for client in clients:
        identity = (
            supabase
            .table("client_identities")
            .select("first_name, last_name, email")
            .eq("client_id", client["id"])
            .maybe_single()
            .execute()
            .data
        )

        results.append({
            "client_id": client["id"],
            "display_code": client["display_code"],
            "first_name": identity.get("first_name") if identity else client["display_code"],
            "last_name": identity.get("last_name") if identity else "",
            "email": identity.get("email") if identity else "",
            "programme": client.get("programme"),
            "status": client.get("status"),
        })

    return results