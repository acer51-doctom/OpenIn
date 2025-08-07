async function sendNativeMessage(message) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendNativeMessage(
      "com.example.openurl",
      message,
      (response) => {
        if (chrome.runtime.lastError) {
          reject(chrome.runtime.lastError.message);
        } else {
          resolve(response);
        }
      }
    );
  });
}

async function init() {
  const container = document.getElementById("buttons");

  try {
    const response = await sendNativeMessage({ action: "get_browsers" });
    const browsers = response.browsers;

    if (!browsers || browsers.length === 0) {
      container.innerHTML = "No supported browsers found.";
      return;
    }

    container.innerHTML = "";
    browsers.forEach(browser => {
      const btn = document.createElement("button");
      btn.textContent = browser;
      btn.addEventListener("click", async () => {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        try {
          await sendNativeMessage({
            action: "open_url",
            browser,
            url: tab.url
          });
          window.close();
        } catch (err) {
          alert("ERROR! The helper has not been installed.");
        }
      });
      container.appendChild(btn);
    });
  } catch (err) {
    container.innerHTML = `
      <div style="color: red;">
        ERROR! The helper has not been installed.<br><br>
        Please install it from:<br>
        <a href="https://github.com/acer51-doctom/openin" target="_blank">Install Instructions</a>
      </div>
    `;
  }
}

init();
