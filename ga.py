"""구글 애널리틱스(GA4) 연결.

Streamlit은 페이지 <head>를 직접 고칠 수 없어서, 보이지 않는 작은 칸(높이 0)에
GA 코드를 넣고, 주소에 붙은 UTM 꼬리표를 GA에 함께 넘긴다.
측정 ID(G-로 시작)는 공개돼도 괜찮은 값이다.
"""
import json
import re
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
            # UTM 규칙(영문·숫자·. _ -)만 남겨서, 주소에 이상한 코드를 넣어도 실행되지 않게 한다
            safe = re.sub(r"[^a-z0-9._-]", "", str(value).lower())[:100]
            if safe:
                out[key] = safe
    return out


def inject_ga() -> None:
    if not MEASUREMENT_ID.startswith("G-") or "X" * 6 in MEASUREMENT_ID:
        return
    utm = _utm_from_url()
    query = urlencode(utm)
    page_location = LANDING_URL + (("?" + query) if query else "")
    names = {"utm_source": "campaign_source", "utm_medium": "campaign_medium", "utm_campaign": "campaign_name", "utm_content": "campaign_content", "utm_term": "campaign_term"}
    params = {names[k]: v for k, v in utm.items()}

    inline = (
        "window.dataLayer=window.dataLayer||[];"
        "function gtag(){dataLayer.push(arguments);}"
        "gtag('js',new Date());"
        f"gtag('config',{json.dumps(MEASUREMENT_ID)},"
        f"{{page_location:{json.dumps(page_location)},page_title:'hello_streamlit'}});"
        f"gtag('event','landing_view',{json.dumps(params)});"
    )
    components.html(
        f"""
<script>
(function () {{
  var w = window.parent, d = w.document;
  if (w.__gaInjected) return;
  w.__gaInjected = true;
  var lib = d.createElement('script');
  lib.async = true;
  lib.src = 'https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}';
  d.head.appendChild(lib);
  var init = d.createElement('script');
  init.text = {json.dumps(inline)};
  d.head.appendChild(init);
}})();
</script>
""",
        height=0,
    )
