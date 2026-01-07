# FastAPI Project - Dashboard

The dashboard is built with [Vite](https://vitejs.dev/), [React](https://reactjs.org/), [TypeScript](https://www.typescriptlang.org/), [TanStack Query](https://tanstack.com/query), [TanStack Router](https://tanstack.com/router) and [Chakra UI](https://chakra-ui.com/).

## Dashboard development

Before you begin, ensure that you have either the Node Version Manager (nvm) or Fast Node Manager (fnm) installed on your system.

* To install fnm follow the [official fnm guide](https://github.com/Schniz/fnm#installation). If you prefer nvm, you can install it using the [official nvm guide](https://github.com/nvm-sh/nvm#installing-and-updating).

* After installing either nvm or fnm, proceed to the `dashboard` directory:

```bash
cd dashboard
```
* If the Node.js version specified in the `.nvmrc` file isn't installed on your system, you can install it using the appropriate command:

```bash
# If using fnm
fnm install

# If using nvm
nvm install
```

* Once the installation is complete, switch to the installed version:

```bash
# If using fnm
fnm use

# If using nvm
nvm use
```

* Within the `dashboard` directory, install the necessary NPM packages:

```bash
npm install
```

* And start the live server with the following `npm` script:

```bash
npm run dev
```

* Then open your browser at http://localhost:5173/.

Notice that this live server is not running inside Docker, it's for local development, and that is the recommended workflow. Once you are happy with your dashboard, you can build the dashboard Docker image and start it, to test it in a production-like environment. But building the image at every change will not be as productive as running the local development server with live reload.

Check the file `package.json` to see other available options.

### Removing the dashboard

If you are developing an API-only app and want to remove the dashboard, you can do it easily:

* Remove the `./dashboard` directory.

* In the `docker-compose.yml` file, remove the whole service / section `dashboard`.

* In the `docker-compose.override.yml` file, remove the whole service / section `dashboard` and `playwright`.

Done, you have a dashboard-less (api-only) app. 🤓

---

If you want, you can also remove the `DASHBOARD` environment variables from:

* `.env`
* `./scripts/*.sh`

But it would be only to clean them up, leaving them won't really have any effect either way.

## Generate Client

### Automatically

* Activate the backend virtual environment.
* From the top level project directory, run the script:

```bash
./scripts/generate-client.sh
```

* Commit the changes.

### Manually

* Start the Docker Compose stack.

* Download the OpenAPI JSON file from `http://localhost/api/v1/openapi.json` and copy it to a new file `openapi.json` at the root of the `dashboard` directory.

* To generate the dashboard client, run:

```bash
npm run generate-client
```

* Commit the changes.

Notice that everytime the backend changes (changing the OpenAPI schema), you should follow these steps again to update the dashboard client.

## Using a Remote API

If you want to use a remote API, you can set the environment variable `VITE_API_URL` to the URL of the remote API. For example, you can set it in the `dashboard/.env` file:

```env
VITE_API_URL=https://api.my-domain.example.com
```

Then, when you run the dashboard, it will use that URL as the base URL for the API.

## Code Structure (Dashboard)

The dashboard code is structured as follows:

* `dashboard/src` - The main dashboard code.
* `dashboard/src/assets` - Static assets.
* `dashboard/src/client` - The generated OpenAPI client.
* `dashboard/src/components` -  The different components of the dashboard.
* `dashboard/src/hooks` - Custom hooks.
* `dashboard/src/routes` - The different routes of the dashboard which include the pages.
* `theme.tsx` - The Chakra UI custom theme.

## End-to-End Testing with Playwright

The dashboard includes initial end-to-end tests using Playwright. To run the tests, you need to have the Docker Compose stack running. Start the stack with the following command:

```bash
docker compose up -d --wait backend
```

Then, you can run the tests with the following command:

```bash
npx playwright test
```

You can also run your tests in UI mode to see the browser and interact with it running:

```bash
npx playwright test --ui
```

To stop and remove the Docker Compose stack and clean the data created in tests, use the following command:

```bash
docker compose down -v
```

To update the tests, navigate to the tests directory and modify the existing test files or add new ones as needed.

For more information on writing and running Playwright tests, refer to the official [Playwright documentation](https://playwright.dev/docs/intro).
