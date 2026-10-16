"""구글 애널리틱스(GA4) 연결.

Streamlit은 페이지 <head>를 직접 고칠 수 없어서, 보이지 않는 작은 칸(높이 0)에
GA 코드를 넣고, 주소에 붙은 UTM 꼬리표를 GA에 함께 넘긴다.
측정 ID(G-로 시작)는 공개돼도 괜찮은 값이다.
"""
import json
from urllib.parse import urlencode

import streamlit as st
import streamlit.components.v1 as components

MEASUREMENT_ID = "G-2KLL5V7ECJ"  # GA 웹 스트림의 측정 ID
LANDING_URL = "https://helloapp-ajoqd4ielht8xjeqs77toz.streamlit.app/"
UTM_KEYS = ("utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term")


def _utm_from_url() -> dict:
    out = {}
    for key in UTM_KEYS:
        value = st.query_params.get(key)
        if value:
            out[key] = str(value)[:100]
    return out


def inject_ga() -> None:
    if not MEASUREMENT_ID.startswith("G-") or "X" * 6 in MEASUREMENT_ID:
        return
    utm = _utm_from_url()
    query = urlencode(utm)
    page_location = LANDING_URL + (("?" + query) if query else "")
    params = {k.replace("utm_", "campaign_"): v for k, v in utm.items()}

    components.html(
        f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', {json.dumps(MEASUREMENT_ID)}, {{
    page_location: {json.dumps(page_location)},
    page_title: 'hello_streamlit'
  }});
  gtag('event', 'landing_view', {json.dumps(params)});
</script>
""",
        height=0,
    )
