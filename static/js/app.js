/**
 * Email Scam Detector - Frontend Application
 * Handles UI interactions, API calls, and data visualization
 */

const APP_CONFIG = {
    API_BASE: "/api",
    UPDATE_INTERVAL: 5000,
    CHART_OPTIONS: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                labels: {
                    color: "#cbd5e1",
                    font: { size: 12, weight: 600 },
                    padding: 15,
                },
            },
        },
        scales: {
            y: {
                ticks: { color: "#94a3b8" },
                grid: { color: "rgba(255, 255, 255, 0.05)" },
            },
            x: {
                ticks: { color: "#94a3b8" },
                grid: { color: "rgba(255, 255, 255, 0.05)" },
            },
        },
    },
};

let charts = {
    risk: null,
    classification: null,
};

// ============================================================================
// Initialization
// ============================================================================

document.addEventListener("DOMContentLoaded", async () => {
    console.log("Application initializing...");
    
    // Setup event listeners
    setupEventListeners();
    
    // Check health and initialize
    await checkAppHealth();
    
    // Load initial data
    await loadStats();
    await loadModelInfo();
    await loadHistory();
    
    // Setup auto-refresh
    setInterval(async () => {
        await loadStats();
        await loadHistory();
    }, APP_CONFIG.UPDATE_INTERVAL);
    
    // Update footer time
    updateFooterTime();
    setInterval(updateFooterTime, 1000);
    
    console.log("Application ready");
});

function setupEventListeners() {
    const analyzeBtn = document.getElementById("analyzeBtn");
    const clearBtn = document.getElementById("clearBtn");
    const emailInput = document.getElementById("emailInput");
    
    if (analyzeBtn) {
        analyzeBtn.addEventListener("click", analyzeEmail);
    }
    
    if (clearBtn) {
        clearBtn.addEventListener("click", clearInput);
    }
    
    if (emailInput) {
        emailInput.addEventListener("keydown", (e) => {
            if (e.ctrlKey && e.key === "Enter") {
                analyzeEmail();
            }
        });
    }
}

// ============================================================================
// Health Check & Status
// ============================================================================

async function checkAppHealth() {
    try {
        const response = await fetch(`${APP_CONFIG.API_BASE}/health`);
        const data = await response.json();
        
        const statusIndicator = document.getElementById("statusIndicator");
        const statusDot = statusIndicator?.querySelector(".status-dot");
        const statusText = statusIndicator?.querySelector(".status-text");
        
        if (statusDot) {
            if (data.status === "healthy") {
                statusDot.classList.add("healthy");
                statusText.textContent = "System Ready";
            } else if (data.status === "degraded") {
                statusDot.style.background = "#f59e0b";
                statusText.textContent = "Limited Functionality";
            } else {
                statusDot.style.background = "#ef4444";
                statusText.textContent = "System Error";
            }
        }
        
        console.log("Health status:", data);
    } catch (error) {
        console.error("Health check failed:", error);
        updateStatus("System Error", false);
    }
}

function updateStatus(text, healthy = true) {
    const statusDot = document.querySelector(".status-dot");
    const statusText = document.querySelector(".status-text");
    
    if (statusDot) {
        statusDot.style.background = healthy ? "#10b981" : "#ef4444";
    }
    if (statusText) {
        statusText.textContent = text;
    }
}

// ============================================================================
// Email Analysis
// ============================================================================

async function analyzeEmail() {
    try {
        const emailInput = document.getElementById("emailInput");
        const email = emailInput.value.trim();
        
        // Validation
        if (!email) {
            showError("Please enter an email to analyze");
            return;
        }
        
        if (email.length < 5) {
            showError("Email content must be at least 5 characters");
            return;
        }
        
        if (email.length > 50000) {
            showError("Email content exceeds maximum length (50000 characters)");
            return;
        }
        
        // Show loading
        const loadingIndicator = document.getElementById("loadingIndicator");
        const resultContainer = document.getElementById("resultContainer");
        const errorContainer = document.getElementById("errorContainer");
        
        if (loadingIndicator) loadingIndicator.style.display = "flex";
        if (resultContainer) resultContainer.style.display = "none";
        if (errorContainer) errorContainer.style.display = "none";
        
        // Make API call
        const response = await fetch(`${APP_CONFIG.API_BASE}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email }),
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Prediction failed");
        }
        
        const result = await response.json();
        
        // Hide loading
        if (loadingIndicator) loadingIndicator.style.display = "none";
        
        // Display result
        displayResult(result);
        
        // Refresh stats
        await loadStats();
        await loadHistory();
        
    } catch (error) {
        console.error("Error analyzing email:", error);
        const loadingIndicator = document.getElementById("loadingIndicator");
        if (loadingIndicator) loadingIndicator.style.display = "none";
        showError(error.message || "An error occurred during analysis");
    }
}

function displayResult(result) {
    try {
        const resultCard = document.getElementById("resultCard");
        const resultContainer = document.getElementById("resultContainer");
        
        const isScam = result.classification.includes("PHISHING");
        const riskLevel = result.risk_level;
        
        // Determine colors based on risk
        let riskColor = "#3b82f6";
        let riskEmoji = "⚠️";
        
        if (riskLevel === "CRITICAL") {
            riskColor = "#dc2626";
            riskEmoji = "🚨";
        } else if (riskLevel === "HIGH") {
            riskColor = "#ef4444";
            riskEmoji = "🔴";
        } else if (riskLevel === "MEDIUM") {
            riskColor = "#f59e0b";
            riskEmoji = "🟠";
        } else if (riskLevel === "LOW") {
            riskColor = "#eab308";
            riskEmoji = "🟡";
        } else if (riskLevel === "SAFE") {
            riskColor = "#10b981";
            riskEmoji = "✅";
        }
        
        const html = `
            <div class="result-header">
                <div class="result-icon">${riskEmoji}</div>
                <div class="result-title-section">
                    <h3 style="color: ${riskColor};">${result.classification}</h3>
                    <p>${result.risk_level} RISK - ${new Date(result.timestamp).toLocaleTimeString()}</p>
                </div>
            </div>
            
            <div class="result-grid">
                <div class="result-item">
                    <div class="result-label">Confidence</div>
                    <div class="result-value" style="color: ${riskColor};">${result.confidence_score}%</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Risk Level</div>
                    <div class="result-value" style="color: ${riskColor};">${result.risk_level}</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Analysis Type</div>
                    <div class="result-value">${isScam ? "🚨" : "✅"}</div>
                </div>
            </div>
            
            <div class="threat-summary">
                <strong>🔍 Threat Analysis:</strong><br>
                ${result.threat_summary}
            </div>
            
            <div class="threat-summary" style="margin-top: 15px; border-left-color: #60a5fa;">
                <strong>📧 Email Preview:</strong><br>
                ${escapeHtml(result.email_preview)}
            </div>
        `;
        
        if (resultCard) {
            resultCard.innerHTML = html;
            resultCard.className = `result-card ${isScam ? "threat" : "safe"}`;
        }
        
        if (resultContainer) {
            resultContainer.style.display = "block";
        }
        
        // Scroll to result
        setTimeout(() => {
            resultContainer?.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }, 100);
        
    } catch (error) {
        console.error("Error displaying result:", error);
        showError("Error displaying analysis result");
    }
}

function clearInput() {
    const emailInput = document.getElementById("emailInput");
    const resultContainer = document.getElementById("resultContainer");
    const errorContainer = document.getElementById("errorContainer");
    
    if (emailInput) emailInput.value = "";
    if (resultContainer) resultContainer.style.display = "none";
    if (errorContainer) errorContainer.style.display = "none";
    
    emailInput?.focus();
}

function showError(message) {
    const errorContainer = document.getElementById("errorContainer");
    const errorMessage = document.getElementById("errorMessage");
    const resultContainer = document.getElementById("resultContainer");
    
    if (errorMessage) {
        errorMessage.textContent = `❌ ${message}`;
    }
    
    if (errorContainer) {
        errorContainer.style.display = "block";
    }
    
    if (resultContainer) {
        resultContainer.style.display = "none";
    }
}

// ============================================================================
// Statistics & Data Loading
// ============================================================================

async function loadStats() {
    try {
        const response = await fetch(`${APP_CONFIG.API_BASE}/stats`);
        const data = await response.json();
        const stats = data.stats || {};
        
        // Update stat displays
        const totalStats = document.getElementById("totalStats");
        const scamStats = document.getElementById("scamStats");
        const legitimateStats = document.getElementById("legitimateStats");
        const confidenceStats = document.getElementById("confidenceStats");
        
        if (totalStats) totalStats.textContent = stats.total_predictions || 0;
        if (scamStats) scamStats.textContent = stats.scam_detected || 0;
        if (legitimateStats) legitimateStats.textContent = stats.legitimate || 0;
        if (confidenceStats) confidenceStats.textContent = `${stats.average_confidence || 0}%`;
        
        // Update charts
        updateCharts(stats.risk_distribution || {}, stats);
        
    } catch (error) {
        console.error("Error loading stats:", error);
    }
}

async function loadModelInfo() {
    try {
        const response = await fetch(`${APP_CONFIG.API_BASE}/metrics`);
        const data = await response.json();
        const metrics = data.metrics || {};
        const bestModel = data.best_model || "Unknown";
        
        const modelInfo = document.getElementById("modelInfo");
        if (!modelInfo) return;
        
        if (Object.keys(metrics).length === 0) {
            modelInfo.innerHTML = "<p class='loading-text'>Training model...</p>";
            return;
        }
        
        let html = `
            <div class="metric-row">
                <span class="metric-name">Best Model</span>
                <span class="metric-value">${bestModel}</span>
            </div>
        `;
        
        for (const [model, values] of Object.entries(metrics)) {
            html += `
                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255, 255, 255, 0.05);">
                    <div style="font-weight: 600; color: #60a5fa; margin-bottom: 10px;">${model}</div>
                    <div class="metric-row">
                        <span class="metric-name">Accuracy</span>
                        <span class="metric-value">${(values.accuracy * 100).toFixed(1)}%</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-name">F1-Score</span>
                        <span class="metric-value">${(values.f1 * 100).toFixed(1)}%</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-name">Precision</span>
                        <span class="metric-value">${(values.precision * 100).toFixed(1)}%</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-name">Recall</span>
                        <span class="metric-value">${(values.recall * 100).toFixed(1)}%</span>
                    </div>
                </div>
            `;
        }
        
        modelInfo.innerHTML = html;
        
    } catch (error) {
        console.error("Error loading model info:", error);
    }
}

async function loadHistory() {
    try {
        const response = await fetch(`${APP_CONFIG.API_BASE}/history`);
        const data = await response.json();
        const history = data.history || [];
        
        const historyList = document.getElementById("historyList");
        if (!historyList) return;
        
        if (history.length === 0) {
            historyList.innerHTML = "<p class='empty-state'>No analysis history yet</p>";
            return;
        }
        
        let html = "";
        history.slice().reverse().slice(0, 20).forEach((item) => {
            const isScam = item.classification?.includes("PHISHING");
            const riskLevel = item.risk_level || "UNKNOWN";
            const timestamp = new Date(item.timestamp);
            const timeStr = timestamp.toLocaleTimeString();
            
            html += `
                <div class="history-item ${isScam ? "threat" : "safe"}">
                    <div class="history-time">${timeStr}</div>
                    <div class="history-text">
                        <strong>${item.classification || "Unknown"}</strong>
                    </div>
                    <div style="font-size: 12px; color: #94a3b8; margin-bottom: 5px;">
                        ${item.email_preview || "No preview"}
                    </div>
                    <div class="history-confidence">
                        ${riskLevel} • ${item.confidence_score}%
                    </div>
                </div>
            `;
        });
        
        historyList.innerHTML = html;
        
    } catch (error) {
        console.error("Error loading history:", error);
    }
}

// ============================================================================
// Charts
// ============================================================================

function updateCharts(riskDistribution, stats) {
    updateRiskChart(riskDistribution);
    updateClassificationChart(stats);
}

function updateRiskChart(riskDistribution) {
    try {
        const ctx = document.getElementById("riskChart");
        if (!ctx) return;
        
        const labels = Object.keys(riskDistribution).sort();
        const data = labels.map((label) => riskDistribution[label] || 0);
        
        const colors = {
            CRITICAL: "#dc2626",
            HIGH: "#ef4444",
            MEDIUM: "#f59e0b",
            LOW: "#eab308",
            SAFE: "#10b981",
        };
        
        const backgroundColors = labels.map((label) => colors[label] || "#3b82f6");
        
        // Destroy existing chart
        if (charts.risk) {
            charts.risk.destroy();
        }
        
        charts.risk = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels,
                datasets: [
                    {
                        data,
                        backgroundColor: backgroundColors,
                        borderColor: "rgba(255, 255, 255, 0.1)",
                        borderWidth: 2,
                    },
                ],
            },
            options: {
                ...APP_CONFIG.CHART_OPTIONS,
                plugins: {
                    ...APP_CONFIG.CHART_OPTIONS.plugins,
                    legend: {
                        ...APP_CONFIG.CHART_OPTIONS.plugins.legend,
                        position: "bottom",
                    },
                },
            },
        });
        
    } catch (error) {
        console.error("Error updating risk chart:", error);
    }
}

function updateClassificationChart(stats) {
    try {
        const ctx = document.getElementById("classificationChart");
        if (!ctx) return;
        
        const scam = stats.scam_detected || 0;
        const legitimate = stats.legitimate || 0;
        
        // Destroy existing chart
        if (charts.classification) {
            charts.classification.destroy();
        }
        
        charts.classification = new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Threat Detected", "Legitimate"],
                datasets: [
                    {
                        label: "Count",
                        data: [scam, legitimate],
                        backgroundColor: ["#ef4444", "#10b981"],
                        borderColor: ["#dc2626", "#059669"],
                        borderWidth: 2,
                        borderRadius: 8,
                    },
                ],
            },
            options: {
                ...APP_CONFIG.CHART_OPTIONS,
                indexAxis: "y",
                plugins: {
                    ...APP_CONFIG.CHART_OPTIONS.plugins,
                    legend: {
                        ...APP_CONFIG.CHART_OPTIONS.plugins.legend,
                        display: false,
                    },
                },
            },
        });
        
    } catch (error) {
        console.error("Error updating classification chart:", error);
    }
}

// ============================================================================
// Utilities
// ============================================================================

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function updateFooterTime() {
    try {
        const footerTime = document.getElementById("footerTime");
        if (footerTime) {
            const now = new Date();
            footerTime.textContent = `Last updated: ${now.toLocaleTimeString()}`;
        }
    } catch (error) {
        console.error("Error updating footer time:", error);
    }
}

// Log version info
console.log("Email Scam Detector v1.0 - Production Ready");
