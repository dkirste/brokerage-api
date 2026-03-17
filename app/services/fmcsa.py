import logging

import httpx

from app.config import settings
from app.schemas import CarrierVerifyResponse

logger = logging.getLogger(__name__)

FMCSA_BASE = "https://mobile.fmcsa.dot.gov/qc/services/carriers"

# Mock carrier data used when the FMCSA API is unavailable
MOCK_CARRIERS: dict[str, dict] = {
    "55555": {
        "legal_name": "ABC Trucking LLC",
        "dot_number": "1234567",
        "entity_type": "CARRIER",
        "allowed": True,
        "out_of_service": False,
        "insurance_on_file": True,
    },
    "123456": {
        "legal_name": "Fast Freight Inc.",
        "dot_number": "2345678",
        "entity_type": "CARRIER",
        "allowed": True,
        "out_of_service": False,
        "insurance_on_file": True,
    },
    "999999": {
        "legal_name": "Suspended Transport Co.",
        "dot_number": "9999999",
        "entity_type": "CARRIER",
        "allowed": False,
        "out_of_service": True,
        "insurance_on_file": False,
    },
}


def _mock_verify(mc_number: str) -> CarrierVerifyResponse:
    """Return mock carrier data when FMCSA API is unavailable."""
    carrier = MOCK_CARRIERS.get(mc_number)
    if not carrier:
        return CarrierVerifyResponse(
            mc_number=mc_number,
            eligible=False,
            eligibility_reasons=["No carrier found for this MC number (mock)"],
        )

    reasons: list[str] = []
    if not carrier["allowed"]:
        reasons.append("Carrier is not authorized to operate")
    if carrier["out_of_service"]:
        reasons.append("Carrier is out of service")
    if not carrier["insurance_on_file"]:
        reasons.append("No insurance on file")

    eligible = carrier["allowed"] and not carrier["out_of_service"] and carrier["insurance_on_file"]

    return CarrierVerifyResponse(
        mc_number=mc_number,
        legal_name=carrier["legal_name"],
        dot_number=carrier["dot_number"],
        entity_type=carrier["entity_type"],
        operating_status="authorized" if carrier["allowed"] else "not authorized",
        out_of_service=carrier["out_of_service"],
        insurance_on_file=carrier["insurance_on_file"],
        eligible=eligible,
        eligibility_reasons=reasons if reasons else ["Carrier meets all eligibility requirements"],
    )


async def verify_carrier(mc_number: str) -> CarrierVerifyResponse:
    url = f"{FMCSA_BASE}/docket-number/{mc_number}"
    params = {"webKey": settings.FMCSA_API_KEY}

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, params=params)
    except httpx.HTTPError:
        logger.warning("FMCSA API unreachable, falling back to mock data")
        return _mock_verify(mc_number)

    if resp.status_code != 200:
        logger.warning("FMCSA API returned %s, falling back to mock data", resp.status_code)
        return _mock_verify(mc_number)

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
