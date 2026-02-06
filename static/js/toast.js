const MAX_NOTIFICATIONS = 3;
const NOTIFY_TIMEOUT = 10000;

let activeNotifications = [];

window.showNotify = function (
  message,
  title = "Notification",
  options = {}
) {
  const template = document.getElementById("notify-panel");
  if (!template) return;

  //Don’t notify over screensaver
  const screensaver = document.getElementById("screensaver");
  if (screensaver?.classList.contains("show")) return;

  // Clone template
  const panel = template.cloneNode(true);
  panel.removeAttribute("id");
  panel.classList.remove("hidden");

  const titleEl = panel.querySelector("#notify-title");
  const msgEl   = panel.querySelector("#notify-message");
  const iconEl  = panel.querySelector("#notify-icon");

  if (!titleEl || !msgEl || !iconEl) return;

  titleEl.textContent = title;
  msgEl.textContent = message;

  // Avatar / icon handling
  if (options.avatar) {
    iconEl.src = options.avatar;
    iconEl.style.display = "block";
  } else if (options.icon || options.fallbackIcon) {
    iconEl.src = options.icon || options.fallbackIcon;
    iconEl.style.display = "block";
  } else {
    iconEl.style.display = "none";
  }

  // Insert at top of stack
  document.body.appendChild(panel);
  activeNotifications.unshift(panel);

  // Enforce stack limit
  while (activeNotifications.length > MAX_NOTIFICATIONS) {
    const old = activeNotifications.pop();
    old.remove();
  }

  // Apply stack offsets
  activeNotifications.forEach((el, i) => {
    el.classList.remove("stack-0", "stack-1", "stack-2");
    el.classList.add(`stack-${i}`);
  });

  // Animate in
  requestAnimationFrame(() => panel.classList.add("show"));

  // Auto dismiss
  const timeout = options.timeout ?? NOTIFY_TIMEOUT;
  const timer = setTimeout(() => dismissNotify(panel), timeout);

  // Click to dismiss
  panel.onclick = () => {
    clearTimeout(timer);
    dismissNotify(panel);
  };
};

function dismissNotify(panel) {
  panel.classList.remove("show");

  setTimeout(() => {
    panel.remove();
    activeNotifications = activeNotifications.filter(p => p !== panel);

    // Re-stack remaining
    activeNotifications.forEach((el, i) => {
      el.classList.remove("stack-0", "stack-1", "stack-2");
      el.classList.add(`stack-${i}`);
    });
  }, 350);
}
