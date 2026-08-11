const API = "";

async function checkHealth() {
    const health = document.getElementById("health");

    try {
        const response = await fetch(
            `${API}/api/v1/health`
        );

        if (!response.ok) {
            throw new Error("API unavailable");
        }

        health.textContent = "● API ONLINE";
        health.className = "status online";

    } catch (error) {
        health.textContent = "● API OFFLINE";
        health.className = "status offline";
    }
}

async function generateInsight() {

    const button = document.getElementById("generate");
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");

    button.disabled = true;
    button.textContent = "Generating...";
    loading.classList.remove("hidden");
    result.classList.add("hidden");

    const payload = {
        brand_id: document.getElementById("brand").value,

        signal: {
            title: document.getElementById("title").value,

            text: document.getElementById("signal").value,

            category: document.getElementById("category").value,

            signal_type:
                document.getElementById("signalType").value,

            metadata: {
                region: "India",
                source: "dashboard"
            }
        }
    };

    try {

        const response = await fetch(
            `${API}/api/v1/insights`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(payload)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Failed to generate insight"
            );
        }

        renderInsight(data);

    } catch (error) {

        alert(error.message);

    } finally {

        button.disabled = false;
        button.textContent = "Generate Insight";

        loading.classList.add("hidden");
    }
}

function renderInsight(data) {

    document.getElementById("result")
        .classList.remove("hidden");

    document.getElementById("priority")
        .textContent = data.priority;

    document.getElementById("relevance")
        .textContent =
        `${Math.round(data.relevance_score * 100)}%`;

    document.getElementById("confidence")
        .textContent =
        `${Math.round(data.confidence_score * 100)}%`;

    document.getElementById("evidenceCount")
        .textContent = data.evidence_count;

    document.getElementById("grounded")
        .textContent =
        data.grounded
            ? "GROUNDED"
            : "NEEDS EVIDENCE";

    document.getElementById("insightSummary")
        .textContent =
        data.observation;

    document.getElementById("observation")
        .textContent =
        data.observation;

    document.getElementById("interpretation")
        .textContent =
        data.interpretation;

    document.getElementById("opportunity")
        .textContent =
        data.opportunity;

    document.getElementById("risk")
        .textContent =
        data.risk;

    document.getElementById("recommendation")
        .textContent =
        data.recommendation;

    document.getElementById("insightId")
        .textContent =
        data.insight_id;

    document.getElementById("promptVersion")
        .textContent =
        data.prompt_version;

    const evidenceContainer =
        document.getElementById("evidence");

    evidenceContainer.innerHTML = "";

    if (!data.evidence || data.evidence.length === 0) {

        evidenceContainer.innerHTML =
            `<div class="empty">
                No supporting evidence retrieved.
            </div>`;

        return;
    }

    data.evidence.forEach((item) => {

        const element =
            document.createElement("div");

        element.className = "evidence-item";

        element.innerHTML = `
            <strong>${escapeHtml(item.title || "Evidence")}</strong>
            <p>${escapeHtml(item.text || "")}</p>
            <small>
                Source: ${escapeHtml(
                    item.source_type || "database"
                )}
                · Score:
                ${item.score
                    ? Number(item.score).toFixed(3)
                    : "—"}
            </small>
        `;

        evidenceContainer.appendChild(element);
    });
}

function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

checkHealth();