from services.supabase_service import get_supabase


def _safe_execute(query):
    try:
        return query.execute().data
    except Exception as e:
        return {"error": str(e)}


def get_client_summary(display_code: str) -> dict:
    supabase = get_supabase()

    client_res = (
        supabase.table("clients")
        .select("*")
        .eq("display_code", display_code)
        .single()
        .execute()
    )

    client = client_res.data

    if not client:
        return {"error": f"No client found for display_code {display_code}"}

    client_id = client["id"]

    identity = _safe_execute(
        supabase.table("client_identities")
        .select("first_name,last_name,email,gender,date_of_birth,occupation")
        .eq("client_id", client_id)
        .limit(1)
    )

    bloodwork_cycles = _safe_execute(
        supabase.table("bloodwork_cycles")
        .select("*")
        .eq("client_id", client_id)
        .order("draw_date", desc=True)
        .limit(3)
    )

    bloodwork_results = _safe_execute(
        supabase.table("bloodwork_results")
        .select("*")
        .eq("client_id", client_id)
        .limit(50)
    )

    bloodwork_rag = _safe_execute(
        supabase.table("bloodwork_rag_scores")
        .select("*")
        .eq("client_id", client_id)
        .limit(50)
    )

    cgm_metrics = _safe_execute(
        supabase.table("cgm_metrics")
        .select("*")
        .eq("client_id", client_id)
        .order("scored_at", desc=True)
        .limit(5)
    )

    wearable_daily = _safe_execute(
        supabase.table("wearable_daily_summaries")
        .select("*")
        .eq("client_id", client_id)
        .order("summary_date", desc=True)
        .limit(14)
    )

    weekly_checkins = _safe_execute(
        supabase.table("weekly_checkins")
        .select("*")
        .eq("client_id", client_id)
        .order("week_number", desc=True)
        .limit(8)
    )

    monthly_checkins = _safe_execute(
        supabase.table("monthly_checkins")
        .select("*")
        .eq("client_id", client_id)
        .order("month_number", desc=True)
        .limit(6)
    )

    coaching_notes = _safe_execute(
        supabase.table("coaching_session_notes")
        .select("*")
        .eq("client_id", client_id)
        .order("session_date", desc=True)
        .limit(5)
    )

    ongoing_notes = _safe_execute(
        supabase.table("client_ongoing_notes")
        .select("*")
        .eq("client_id", client_id)
        .order("note_date", desc=True)
        .limit(10)
    )

    person_model = _safe_execute(
        supabase.table("client_person_model")
        .select("*")
        .eq("client_id", client_id)
        .order("created_at", desc=True)
        .limit(20)
    )

    decisions = _safe_execute(
        supabase.table("client_decisions")
        .select("*")
        .eq("client_id", client_id)
        .order("decision_date", desc=True)
        .limit(10)
    )

    interactions = _safe_execute(
        supabase.table("client_interactions")
        .select("interaction_ts,source_type,direction,title,summary,tags")
        .eq("client_id", client_id)
        .order("interaction_ts", desc=True)
        .limit(10)
    )

    return {
        "client": client,
        "identity": identity,
        "bloodwork": {
            "cycles": bloodwork_cycles,
            "results": bloodwork_results,
            "rag_scores": bloodwork_rag,
        },
        "cgm": {
            "metrics": cgm_metrics,
        },
        "wearables": {
            "daily_summaries": wearable_daily,
        },
        "checkins": {
            "weekly": weekly_checkins,
            "monthly": monthly_checkins,
        },
        "notes": {
            "coaching_sessions": coaching_notes,
            "ongoing": ongoing_notes,
        },
        "person_model": person_model,
        "decisions": decisions,
        "recent_interactions": interactions,
    }
