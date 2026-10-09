(function () {
  var CATEGORIES = ["ECD Centre", "Bakery", "Plumbing"];
  var SCHEMA_VERSION = "0.2";
  var CONTACT_LABEL = "Demo enquiry only";
  var EXPORT_NOTE = "Exporting this file does not publish a public profile. Public publication in this version is a controlled static build and deploy step.";
  var DEMO_IDS = ["bright-steps-ecd", "sindis-bakery", "ubuntu-plumbing"];

  function el(id) {
    return document.getElementById(id);
  }

  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch];
    });
  }

  function clean(value) {
    return String(value == null ? "" : value).replace(/\s+/g, " ").trim();
  }

  function slug(text) {
    return clean(text).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  }

  function initials(name) {
    var letters = clean(name).split(" ").slice(0, 2).map(function (word) {
      var cleaned = word.replace(/[^A-Za-z0-9]/g, "");
      return cleaned ? cleaned.charAt(0).toUpperCase() : "";
    }).join("");
    return letters || "DZ";
  }

  function announce(message) {
    var notice = el("notice");
    if (!notice) return;
    notice.textContent = message;
  }

  function privateIssues(label, value) {
    var text = String(value == null ? "" : value);
    var issues = [];
    if (/(?:\+|00)27[\s-]?\d/.test(text) || /\b0\d{2}[\s-]?\d{3}[\s-]?\d{4}\b/.test(text)) {
      issues.push(label + ": remove telephone numbers. This demo does not collect them.");
    }
    if (/\b\d{13}\b/.test(text)) {
      issues.push(label + ": remove long identity-number sequences.");
    }
    if (/[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}/i.test(text)) {
      issues.push(label + ": remove email addresses. This demo does not collect them.");
    }
    if (/whatsapp/i.test(text)) {
      issues.push(label + ": remove messaging handles. This demo does not collect them.");
    }
    return issues;
  }

  function offeringLines(value) {
    return String(value == null ? "" : value).split(/\r?\n/).map(function (line) {
      return clean(line);
    }).filter(Boolean);
  }

  function validateDraft(draft) {
    var errors = [];
    var name = clean(draft.name);
    var category = clean(draft.category);
    var area = clean(draft.area);
    var city = clean(draft.city);
    var province = clean(draft.province);
    var summary = clean(draft.summary);
    var hours = clean(draft.hours);
    var offerings = offeringLines(draft.offeringsText);
    var id = slug(name);

    if (!name) errors.push("Enter the organisation name.");
    else if (name.length < 2 || name.length > 80) errors.push("Organisation name must be 2 to 80 characters.");
    if (!category) errors.push("Choose a category.");
    else if (CATEGORIES.indexOf(category) === -1) errors.push("Choose a category from the list.");
    if (!area) errors.push("Enter the area or neighbourhood.");
    else if (area.length < 2 || area.length > 80) errors.push("Area must be 2 to 80 characters.");
    if (!city) errors.push("Enter the city.");
    else if (city.length < 2 || city.length > 80) errors.push("City must be 2 to 80 characters.");
    if (!province) errors.push("Enter the province.");
    else if (province.length < 2 || province.length > 80) errors.push("Province must be 2 to 80 characters.");
    if (!summary) errors.push("Enter what the organisation offers.");
    else if (summary.length < 12) errors.push("Describe the offer in at least 12 characters.");
    else if (summary.length > 280) errors.push("Shorten the description to 280 characters or fewer.");
    if (!hours) errors.push("Enter opening or operating times.");
    else if (hours.length < 2 || hours.length > 80) errors.push("Hours must be 2 to 80 characters.");
    if (offerings.length > 6) errors.push("List at most 6 offerings.");
    offerings.forEach(function (item, index) {
      if (item.length < 2 || item.length > 80) errors.push("Offering " + (index + 1) + " must be 2 to 80 characters.");
    });
    if (!draft.fictionalConfirmed) errors.push("Confirm that this record is fictional.");
    if (!draft.exportConfirmed) errors.push("Confirm that exporting a JSON file does not publish a public profile.");
    if (name && !id) errors.push("Use a name that can become a record id.");

    [name, category, area, city, province, summary, hours].concat(offerings).forEach(function (value, index) {
      var labels = ["Name", "Category", "Area", "City", "Province", "Description", "Hours"];
      var label = index < labels.length ? labels[index] : "Offering";
      privateIssues(label, value).forEach(function (issue) { errors.push(issue); });
    });

    var record = {
      schemaVersion: SCHEMA_VERSION,
      id: id || "profile",
      name: name,
      category: category,
      location: { area: area, city: city, province: province },
      summary: summary,
      hours: hours,
      offerings: offerings,
      contact: { label: CONTACT_LABEL },
      fictional: true,
      publication: { status: "not-published", note: EXPORT_NOTE },
      profilePath: ""
    };

    return { ok: errors.length === 0, errors: errors, record: record };
  }

  function placeLine(location) {
    var parts = [];
    [location.area, location.city, location.province].forEach(function (part) {
      if (part && parts.indexOf(part) === -1) parts.push(part);
    });
    return parts.join(", ");
  }

  function profileCardHtml(record) {
    var place = placeLine(record.location);
    var offerings = (record.offerings || []).map(function (item) {
      return "<li>" + esc(item) + "</li>";
    }).join("");
    return '<div class="business" id="profile"><div class="banner"><div class="avatar" aria-hidden="true">' + esc(initials(record.name)) + '</div><div><span class="tag" style="background:#dafa74">DigiZone Connect · Demo</span><p class="profile-name">' + esc(record.name || "Organisation name") + '</p><p>⌖ ' + esc(place || "Location pending") + '</p></div></div><div class="profile-meta"><span class="pill">' + esc(record.category || "Category pending") + '</span><span class="pill">' + esc(record.location.province || "Province pending") + '</span><span class="pill">◷ ' + esc(record.hours || "Hours pending") + '</span></div><hr class="softline"><h2>About</h2><p>' + esc(record.summary || "Description pending.") + '</p><h2>What is offered</h2><ul class="offerings">' + offerings + '</ul><div class="tip"><strong>How to connect</strong><br>' + esc(CONTACT_LABEL) + '<br><span class="small">Demonstration only. No message is sent and no telephone number is published.</span></div><p class="small">Fictional profile. Information is not independently verified. Exporting this preview does not create a live listing.</p></div>';
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).then(function () {
        announce("Copied to clipboard.");
      }).catch(function () {
        return fallbackCopy(text);
      });
    }
    return fallbackCopy(text);
  }

  function selectVisible(text) {
    var nodes = [el("profile-url"), el("record-view")];
    for (var i = 0; i < nodes.length; i += 1) {
      var node = nodes[i];
      if (!node || node.textContent !== text) continue;
      var range = document.createRange();
      range.selectNodeContents(node);
      var selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      return true;
    }
    return false;
  }

  function fallbackCopy(text) {
    var area = document.createElement("textarea");
    area.value = text;
    document.body.appendChild(area);
    area.select();
    var copied = false;
    try { copied = document.execCommand("copy"); } catch (error) { copied = false; }
    area.remove();
    if (copied) {
      announce("Copied to clipboard.");
      return Promise.resolve();
    }
    if (selectVisible(text)) {
      announce("Copy was blocked. The text is selected — use your device copy command.");
      return Promise.resolve();
    }
    announce("Copy was blocked. Select the profile link and copy it manually.");
    return Promise.resolve();
  }

  function download(name, content, type) {
    var link = document.createElement("a");
    var blob = new Blob([content], { type: type });
    var url = URL.createObjectURL(blob);
    link.href = url;
    link.download = name;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function pageUrl() {
    return location.href.split("#")[0];
  }

  function initDirectory() {
    var search = el("search");
    var category = el("category-filter");
    var locationFilter = el("location-filter");
    var cards = Array.prototype.slice.call(document.querySelectorAll("#directory .entry"));
    var empty = el("empty");
    var count = el("count");
    var params = new URLSearchParams(location.search);

    function optionExists(select, value) {
      return Array.prototype.some.call(select.options, function (option) { return option.value === value; });
    }

    if (params.get("q")) search.value = params.get("q");
    if (params.get("category") && optionExists(category, params.get("category"))) category.value = params.get("category");
    if (params.get("location") && optionExists(locationFilter, params.get("location"))) locationFilter.value = params.get("location");

    function matches(card) {
      var query = search.value.trim().toLowerCase();
      if (category.value !== "all" && card.dataset.category !== category.value) return false;
      if (locationFilter.value !== "all" && card.dataset.area !== locationFilter.value && card.dataset.city !== locationFilter.value) return false;
      if (query && card.dataset.search.toLowerCase().indexOf(query) === -1) return false;
      return true;
    }

    function render() {
      var shown = 0;
      cards.forEach(function (card) {
        var visible = matches(card);
        card.hidden = !visible;
        if (visible) shown += 1;
      });
      empty.hidden = shown !== 0;
      count.textContent = shown === 1 ? "1 shown" : shown + " shown";
      var next = new URLSearchParams();
      if (search.value.trim()) next.set("q", search.value.trim());
      if (category.value !== "all") next.set("category", category.value);
      if (locationFilter.value !== "all") next.set("location", locationFilter.value);
      var query = next.toString();
      history.replaceState(null, "", location.pathname + (query ? "?" + query : ""));
    }

    search.addEventListener("input", render);
    category.addEventListener("change", render);
    locationFilter.addEventListener("change", render);
    render();
  }

  function initProfile() {
    var urlNode = el("profile-url");
    if (urlNode) urlNode.textContent = pageUrl();
    var copyButton = el("copy-url");
    var shareButton = el("share");
    if (copyButton) copyButton.addEventListener("click", function () { copyText(pageUrl()); });
    if (shareButton) shareButton.addEventListener("click", function () {
      var url = pageUrl();
      var title = document.body.dataset.name || document.title;
      var payload = { title: title + " — DEMO", text: "Fictional DigiZone Connect profile. Not a live listing.", url: url };
      if (navigator.share) {
        navigator.share(payload).then(function () {
          announce("Share sheet opened.");
        }).catch(function (error) {
          if (error && error.name === "AbortError") return;
          copyText(url);
        });
        return;
      }
      copyText(url);
    });
  }

  function draftFromForm() {
    return {
      name: el("org-name").value,
      category: el("org-category").value,
      area: el("org-area").value,
      city: el("org-city").value,
      province: el("org-province").value,
      summary: el("org-summary").value,
      hours: el("org-hours").value,
      offeringsText: el("org-offerings").value,
      fictionalConfirmed: el("confirm-fictional").checked,
      exportConfirmed: el("confirm-export").checked
    };
  }

  function showErrors(errors) {
    var box = el("errors");
    if (!errors.length) {
      box.hidden = true;
      box.innerHTML = "";
      return;
    }
    box.hidden = false;
    box.innerHTML = "<p><strong>Complete the record before export.</strong></p><ul>" + errors.map(function (error) {
      return "<li>" + esc(error) + "</li>";
    }).join("") + "</ul>";
  }

  function initCapture() {
    var form = el("capture-form");
    var preview = el("profile-preview");
    var recordView = el("record-view");
    var idView = el("record-id");
    var attempted = false;

    function refresh() {
      var result = validateDraft(draftFromForm());
      preview.innerHTML = profileCardHtml(result.record);
      idView.textContent = result.record.id;
      if (attempted) showErrors(result.ok ? [] : result.errors);
      return result;
    }

    form.addEventListener("input", refresh);
    form.addEventListener("change", refresh);
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      attempted = true;
      var result = refresh();
      if (!result.ok) {
        announce("Export blocked. Complete the missing items listed above.");
        recordView.textContent = "";
        return;
      }
      var json = JSON.stringify(result.record, null, 2) + "\n";
      recordView.textContent = json;
      download(result.record.id + ".json", json, "application/json");
      var collision = DEMO_IDS.indexOf(result.record.id) !== -1;
      announce(collision
        ? "JSON file downloaded. It is not published. This id is already used by a static demo page, and the download does not replace that page."
        : "JSON file downloaded to this device. It is not published. A public profile still needs a controlled static build and deploy.");
    });

    el("copy-json").addEventListener("click", function () {
      attempted = true;
      var result = refresh();
      if (!result.ok) {
        announce("Copy blocked. Complete the missing items listed above.");
        return;
      }
      var json = JSON.stringify(result.record, null, 2) + "\n";
      recordView.textContent = json;
      copyText(json);
    });

    refresh();
  }

  document.addEventListener("DOMContentLoaded", function () {
    var page = document.body.dataset.page;
    if (page === "directory") initDirectory();
    if (page === "profile") initProfile();
    if (page === "capture") initCapture();
  });

  window.DigiZoneConnect = {
    validateDraft: validateDraft,
    slug: slug,
    categories: CATEGORIES,
    exportNote: EXPORT_NOTE
  };
})();
