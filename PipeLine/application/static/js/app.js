(function () {
  "use strict";

  var applications = [
    { id: 1, company: "Linear", role: "Senior Product Designer", status: "Interview", applied: "Jun 12, 2025", initials: "LI", logoStyle: "plum" },
    { id: 2, company: "Figma", role: "Product Designer, Growth", status: "Phone Screen", applied: "Jun 10, 2025", initials: "FI", logoStyle: "coral" },
    { id: 3, company: "Notion", role: "Staff Product Designer", status: "Offer", applied: "Jun 08, 2025", initials: "NO", logoStyle: "ink" },
    { id: 4, company: "Arc", role: "Product Designer", status: "Applied", applied: "Jun 06, 2025", initials: "AR", logoStyle: "blue" },
    { id: 5, company: "Airbnb", role: "Experience Designer", status: "Interview", applied: "Jun 04, 2025", initials: "AI", logoStyle: "rejected" },
    { id: 6, company: "Dropbox", role: "Senior UX Designer", status: "Rejected", applied: "May 28, 2025", initials: "DB", logoStyle: "accent" },
    { id: 7, company: "Vercel", role: "Design Systems Lead", status: "Applied", applied: "May 25, 2025", initials: "VE", logoStyle: "ink" }
  ];

  var activeId = null;
  var toastTimer;
  var statusClass = function (status) { return "status-" + status.toLowerCase().replace(/\s+/g, "-"); };
  var query = function (selector, root) { return (root || document).querySelector(selector); };
  var all = function (selector, root) { return Array.prototype.slice.call((root || document).querySelectorAll(selector)); };

  function showToast(message) {
    var region = query("[data-toast-region]");
    if (!region) return;
    region.textContent = message;
    region.classList.add("is-visible");
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(function () { region.classList.remove("is-visible"); }, 3000);
  }

  function openModal(modal) {
    if (!modal) return;
    modal.classList.remove("is-hidden");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function closeModals() {
    all(".modal-backdrop").forEach(function (modal) {
      modal.classList.add("is-hidden");
      modal.setAttribute("aria-hidden", "true");
    });
    document.body.style.overflow = "";
  }

  function findApplication(id) {
    return applications.find(function (item) { return String(item.id) === String(id); });
  }

  function setDetail(application) {
    if (!application) return;
    activeId = application.id;
    var mark = query("[data-detail-mark]");
    mark.textContent = application.initials;
    mark.className = "company-mark mark-" + application.logoStyle;
    query("[data-detail-company]").textContent = application.company;
    query("[data-detail-role]").textContent = application.role;
    var status = query("[data-detail-status]");
    status.textContent = application.status;
    status.className = "status-badge " + statusClass(application.status);
    query("[data-detail-date]").textContent = application.applied;
    openModal(query("[data-detail-modal]"));
  }

  function openApplicationForm(application) {
    var form = query("[data-application-form]");
    if (!form) return;
    query("[data-form-title]").textContent = application ? "Edit application" : "Add an application";
    query("[data-form-submit]").textContent = application ? "Save changes" : "Save application";
    query("[data-form-id]").value = application ? application.id : "";
    query("[data-form-company]").value = application ? application.company : "";
    query("[data-form-role]").value = application ? application.role : "";
    query("[data-form-status]").value = application ? application.status : "Applied";
    query("[data-form-date]").value = application ? application.applied : "";
    openModal(query("[data-add-modal]"));
    window.setTimeout(function () { query("[data-form-company]").focus(); }, 50);
  }

  function renderRows() {
    var list = query("[data-application-list]");
    if (!list) return;
    var selectedStatus = query(".filter-pill.is-active");
    var activeStatus = selectedStatus ? selectedStatus.getAttribute("data-status-filter") : "All";
    var search = (query("[data-search]") || { value: "" }).value.toLowerCase().trim();
    var rows = all("[data-application]", list);
    var visible = 0;
    rows.forEach(function (row) {
      var matchesSearch = (row.getAttribute("data-company") + " " + row.getAttribute("data-role")).indexOf(search) !== -1;
      var matchesStatus = activeStatus === "All" || row.getAttribute("data-status") === activeStatus;
      var shouldShow = matchesSearch && matchesStatus;
      row.classList.toggle("is-hidden", !shouldShow);
      if (shouldShow) visible += 1;
    });
    var empty = query("[data-empty-filter]", list);
    if (empty) empty.classList.toggle("is-hidden", visible !== 0);
  }

  function wireEvents() {
    all("[data-open-add]").forEach(function (button) { button.addEventListener("click", function () { openApplicationForm(null); }); });
    all("[data-close-modal]").forEach(function (button) { button.addEventListener("click", closeModals); });
    all(".modal-backdrop").forEach(function (backdrop) {
      backdrop.addEventListener("mousedown", function (event) { if (event.target === backdrop) closeModals(); });
    });
    all("[data-toast]").forEach(function (button) { button.addEventListener("click", function () { showToast(button.getAttribute("data-toast")); }); });
    all("[data-complete-reminder]").forEach(function (button) {
      button.addEventListener("click", function () {
        var row = button.closest("[data-reminder]");
        row.classList.toggle("is-complete");
        showToast(row.classList.contains("is-complete") ? "Reminder marked complete." : "Reminder reopened.");
      });
    });
    all("[data-view-application]").forEach(function (button) { button.addEventListener("click", function () { setDetail(findApplication(button.getAttribute("data-view-application"))); }); });
    all("[data-edit-application]").forEach(function (button) { button.addEventListener("click", function () { openApplicationForm(findApplication(button.getAttribute("data-edit-application"))); }); });
    var detailEdit = query("[data-detail-edit]");
    if (detailEdit) detailEdit.addEventListener("click", function () { closeModals(); openApplicationForm(findApplication(activeId)); });
    var form = query("[data-application-form]");
    if (form) form.addEventListener("submit", function (event) {
      event.preventDefault();
      var id = query("[data-form-id]").value;
      var item = id ? findApplication(id) : null;
      if (item) {
        item.company = query("[data-form-company]").value.trim();
        item.role = query("[data-form-role]").value.trim();
        item.status = query("[data-form-status]").value;
        item.applied = query("[data-form-date]").value.trim();
        showToast("Application updated.");
      } else {
        applications.unshift({
          id: Date.now(),
          company: query("[data-form-company]").value.trim(),
          role: query("[data-form-role]").value.trim(),
          status: query("[data-form-status]").value,
          applied: query("[data-form-date]").value.trim(),
          initials: query("[data-form-company]").value.trim().slice(0, 2).toUpperCase(),
          logoStyle: "accent"
        });
        showToast("Application added to your pipeline.");
      }
      closeModals();
      renderRows();
    });
    var search = query("[data-search]");
    if (search) search.addEventListener("input", renderRows);
    all("[data-status-filter]").forEach(function (button) {
      button.addEventListener("click", function () {
        all("[data-status-filter]").forEach(function (item) { item.classList.remove("is-active"); });
        button.classList.add("is-active");
        renderRows();
      });
    });
  }

  document.addEventListener("keydown", function (event) { if (event.key === "Escape") closeModals(); });
  document.addEventListener("DOMContentLoaded", wireEvents);
})();