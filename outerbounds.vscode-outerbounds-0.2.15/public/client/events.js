/* eslint-disable no-undef */
(function () {
  const vscode = acquireVsCodeApi();

  const connectBtn = document.getElementById("connect");
  connectBtn?.addEventListener("click", () => {
    vscode.postMessage({
      type: "obp.workstationConnect",
      data: connectBtn.getAttribute("data-workstation-id"),
    });
  });

  document
    ?.getElementById("validate-setup-btn")
    ?.addEventListener("click", () => {
      vscode.postMessage({
        type: "obp.outerboundsCheck",
      });
    });

  document
    .getElementById("configure-workstations-btn")
    ?.addEventListener("click", () => {
      vscode.postMessage({
        type: "obp.configureWorkstations",
      });
    });

  document
    .getElementById("refresh-window-btn")
    ?.addEventListener("click", () => {
      vscode.postMessage({
        type: "workbench.action.reloadWindow",
      });
    });
})();
