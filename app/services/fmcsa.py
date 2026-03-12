import httpx

from app.config import settings
from app.schemas import CarrierVerifyResponse

FMCSA_BASE = "https://mobile.fmcsa.dot.gov/qc/services/carriers"


async def verify_carrier(mc_number: str) -> CarrierVerifyResponse:
    url = f"{FMCSA_BASE}/docket-number/{mc_number}"
    params = {"webKey": settings.FMCSA_API_KEY}

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params)

    if resp.status_code != 200:
        return CarrierVerifyResponse(
            mc_number=mc_number,
            eligible=False,
            eligibility_reasons=[f"FMCSA API returned status {resp.status_code}"],
        )

    data = resp.json()
    content = data.get("content")
    if not content or not isinstance(content, list) or len(content) == 0:
        return CarrierVerifyResponse(
            mc_number=mc_number,
            eligible=False,
            eligibility_reasons=["No carrier found for this MC number"],
        )

    carrier = content[0].get("carrier", {})

    legal_name = carrier.get("legalName", "")
    dot_number = str(carrier.get("dotNumber", ""))
    entity_type = carrier.get("entityType", "")
    operating_status = carrier.get("allowedToOperate", "")
    oos_flag = carrier.get("oosFlag", "N")

    # Check insurance from bipd fields
    bipd_insurance = carrier.get("bipdInsuranceOnFile", "")
    insurance_on_file = bipd_insurance.upper() in ("Y", "YES") if bipd_insurance else False

    out_of_service = oos_flag.upper() in ("Y", "YES") if oos_flag else False
    allowed = str(operating_status).upper() in ("Y", "YES")

    reasons: list[str] = []
    if not allowed:
        reasons.append("Carrier is not authorized to operate")
    if out_of_service:
        reasons.append("Carrier is out of service")
    if not insurance_on_file:
        reasons.append("No insurance on file")

    eligible = allowed and not out_of_service and insurance_on_file

    return CarrierVerifyResponse(
        mc_number=mc_number,
        legal_name=legal_name,
        dot_number=dot_number,
        entity_type=entity_type,
        operating_status="authorized" if allowed else "not authorized",
        out_of_service=out_of_service,
        insurance_on_file=insurance_on_file,
        eligible=eligible,
        eligibility_reasons=reasons if reasons else ["Carrier meets all eligibility requirements"],
    )
