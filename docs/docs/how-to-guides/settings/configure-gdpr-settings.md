---
myst:
  html_meta:
    description: "Configure the GDPR consent banner, third-party privacy modules, analytics tracker and privacy policy link."
    keywords: "GDPR, DSGVO, cookie banner, privacy, Google Analytics, Matomo, control panel"
doc_type: how-to
audience: admin
tags: [settings, privacy, gdpr]
---

# Configure GDPR settings

This guide shows you how to configure the cookie consent banner, the third-party privacy modules shown to visitors, the analytics tracker, and the privacy policy link, all from the **GDPR Settings** control panel.

## Prerequisites

- You are logged in with a role that can access **Site Setup** (Manager or Site Administrator).

## Steps

### 1. Open the GDPR Settings control panel

1. Go to **Site Setup**.
2. Under the general settings, open **GDPR Settings**.

![The GDPR Settings control panel, showing the banner toggle, privacy modules, tracker, tracker options, and privacy policy URL fields](/_static/images/gdpr-settings-overview.png)

### 2. Show or hide the banner on first visit

Tick **Show GDPR banner on first visit** to display the cookie consent banner immediately to every visitor. Untick it if you only want visitors to be asked for consent in the context of blocks that need it (for example, a YouTube video block).

### 3. Choose which privacy modules are shown

In **Show privacy settings for**, add or remove the third-party services that visitors can individually allow or block in their privacy preferences. Available options are:

- `tracking`
- `youtube`
- `facebook`
- `google`
- `vimeo`
- `twitter`

By default, `tracking`, `youtube`, `facebook`, and `google` are selected.

### 4. Choose the analytics tracker

In the **Tracker** field, select which analytics service the site should use:

- `google` for Google Analytics.
- `matomo` for Matomo.

Leave it empty if you don't want to enable any analytics tracker.

![The Tracker field's dropdown open, showing the google and matomo options](/_static/images/gdpr-settings-tracker-dropdown.png)

### 5. Configure the tracker options

Click **Open configuration** next to **Tracker options** to open the JSON editor:

![The Tracker options JSON editor modal](/_static/images/gdpr-settings-tracker-options-modal.png)

The modal opens empty. Enter the configuration for the tracker you selected in step 4:

- For Google Analytics:

  ```json
  {
    "id": "G-XXXXXXX",
    "gaOptions": { "anonymizeIp": true }
  }
  ```

- For Matomo:

  ```json
  {
    "id": 1,
    "urlBase": "https://matomo.example.com/"
  }
  ```

Click **Close** to save the JSON and return to the control panel.

### 6. Set the privacy policy URL

In **Privacy policy URL**, enter the path or URL of your privacy policy page, for example `/en/privacy`. The cookie consent banner links to this page.

![The GDPR Settings control panel with a privacy policy URL set](/_static/images/gdpr-settings-privacy-url-set.png)

### 7. Save

Click **Save** in the left toolbar.

## Verification

1. Visit the site as an anonymous user. If you enabled the banner on first visit, it should appear immediately.
2. Open the privacy preferences and confirm that only the modules you selected in step 3 are listed.
3. Click the privacy policy link in the banner and confirm it leads to the page you set in step 6.
4. Accept tracking and confirm that the analytics requests for the tracker you configured (Google Analytics or Matomo) are sent.

## Notes

- These settings apply to the `@kitconcept/volto-dsgvo-banner` add-on bundled with this distribution. Without that add-on installed, this control panel has no effect on the front end.
