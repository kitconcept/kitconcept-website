# Playwright acceptance tests

End-to-end tests driven by Playwright, running against a Plone acceptance
backend with `RobotRemote` enabled and a running Volto frontend.

The helpers use these environment variables:

- `BACKEND_HOST` (default `127.0.0.1`)
- `SITE_ID` (default `plone`)
- `API_PATH` (default `http://${BACKEND_HOST}:55001/${SITE_ID}`)
- `FRONTEND_URL` (default `http://localhost:3000`)

Run the complete suite from the repository root:

```bash
make ci-acceptance-playwright-test
```

For interactive development against already-running acceptance servers:

```bash
make acceptance-playwright-test
```

Install Chromium for Playwright once before running locally:

```bash
make -C frontend install-playwright
```
