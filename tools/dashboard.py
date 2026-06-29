from services.supabase_service import get_supabase


def get_dashboard():

    supabase = get_supabase()

    clients = (
        supabase
        .table("clients")
        .select("display_code,status,programme")
        .limit(20)
        .execute()
        .data
    )

    dashboard = {
        "attention": [],
        "review": [],
        "good": []
    }

    for client in clients:

        item = {
            "display_code": client["display_code"],
            "programme": client.get("programme", ""),
        }

        if client["status"] == "active":
            dashboard["good"].append(item)
        elif client["status"] == "paused":
            dashboard["review"].append(item)
        else:
            dashboard["attention"].append(item)

    return dashboard