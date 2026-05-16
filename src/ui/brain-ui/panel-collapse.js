const STORAGE_L1 = "bailongma-panel-l1-collapsed";
const STORAGE_L2 = "bailongma-panel-l2-collapsed";

function storageKeyForSide(side) {
  return side === "l1" ? STORAGE_L1 : STORAGE_L2;
}

function classForSide(side) {
  return side === "l1" ? "l1-collapsed" : "l2-collapsed";
}

export function initPanelCollapse() {
  function setPanel(side, collapsed) {
    document.body.classList.toggle(classForSide(side), collapsed);
    try { localStorage.setItem(storageKeyForSide(side), collapsed ? "1" : "0"); } catch {}
    // Sync show-btn visibility
    updateShowBtnState();
  }

  function togglePanel(side) {
    const cls = classForSide(side);
    setPanel(side, !document.body.classList.contains(cls));
  }

  // Start both panels collapsed (auto-hide)
  document.body.classList.add("l1-collapsed", "l2-collapsed");

  // Listeners for tab toggle buttons
  document.getElementById("panel-l1-tab")?.addEventListener("click", () => togglePanel("l1"));
  document.getElementById("panel-l2-tab")?.addEventListener("click", () => togglePanel("l2"));

  // Listeners for X close buttons inside panels
  document.getElementById("panel-l1-close")?.addEventListener("click", () => setPanel("l1", true));
  document.getElementById("panel-l2-close")?.addEventListener("click", () => setPanel("l2", true));

  // Keyboard shortcuts
  window.addEventListener("keydown", (event) => {
    if (event.target && (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA" || event.target.isContentEditable)) return;
    if (event.ctrlKey || event.metaKey || event.altKey) return;
    if (event.key === "[") { event.preventDefault(); togglePanel("l1"); }
    if (event.key === "]") { event.preventDefault(); togglePanel("l2"); }
  });

  // Create floating show-all button
  const showBtn = document.createElement("button");
  showBtn.id = "panel-show-all-btn";
  showBtn.className = "panel-show-all";
  showBtn.setAttribute("aria-label", "显示面板");
  showBtn.setAttribute("title", "显示两侧面板");
  showBtn.textContent = "☐";
  document.body.appendChild(showBtn);

  function updateShowBtnState() {
    const l1Hidden = document.body.classList.contains("l1-collapsed");
    const l2Hidden = document.body.classList.contains("l2-collapsed");
    showBtn.style.display = (l1Hidden && l2Hidden) ? "flex" : "none";
  }

  showBtn.addEventListener("click", () => {
    setPanel("l1", false);
    setPanel("l2", false);
  });

  // Click blank center area to hide both panels when both are shown
  document.addEventListener("click", (event) => {
    const l1Hidden = document.body.classList.contains("l1-collapsed");
    const l2Hidden = document.body.classList.contains("l2-collapsed");
    // Only act when both panels are shown
    if (l1Hidden || l2Hidden) return;

    const target = event.target;
    // Don't hide if clicking inside either panel
    if (target.closest("#panel-l1") || target.closest("#panel-l2")) return;
    // Don't hide if clicking the show-all button
    if (target.closest("#panel-show-all-btn")) return;
    // Don't hide if clicking on interactive elements (buttons, inputs, etc.)
    if (target.closest("button, input, textarea, select, [contenteditable]")) return;

    // Clicked on blank center area → hide both panels
    setPanel("l1", true);
    setPanel("l2", true);
  });

  updateShowBtnState();
}
