from services.supabase_service import get_supabase


def get_client_profile(display_code: str):
    supabase = get_supabase()

    client = (
        supabase
        .table("clients")
        .select("id, display_code, programme, status, enrolled_at")
        .eq("display_code", display_code)
        .single()
        .execute()
        .data
    )

    identity = (
        supabase
        .table("client_identities")
        .select("first_name, last_name, email, occupation")
        .eq("client_id", client["id"])
        .single()
        .execute()
        .data
    )

    return {
        "client_id": client["id"],
        "display_code": client["display_code"],
        "name": f"{identity.get('first_name', '')} {identity.get('last_name', '')}".strip(),
        "email": identity.get("email"),
        "occupation": identity.get("occupation"),
        "programme": client.get("programme") or "Not set",
        "status": client.get("status"),
        "enrolled_at": client.get("enrolled_at"),
    }