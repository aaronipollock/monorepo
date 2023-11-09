# Monorepo

<a alt="Nx logo" href="https://nx.dev" target="_blank" rel="noreferrer"><img src="https://raw.githubusercontent.com/nrwl/nx/master/images/nx-logo.png" width="45"></a>

✨ **This workspace has been generated by [Nx, a Smart, fast and extensible build system.](https://nx.dev)** ✨

## Storybook

to run `yarn storybook`
to build `yarn storybook:build`

# Nx Workspace with Expo Application: BetterAngels

### 1. Set Up Google OAuth Locally:

**Important** For OAuth redirects to work locally for **Android** emulator, run:

```
adb reverse tcp:8000 tcp:8000
```

Note: This might require you to install adb (Android Debug Bridge) [Android SDK Platform-Tools](https://developer.android.com/studio/releases/platform-tools)

- **Build** the "betterangels" application:

```
yarn nx build betterangels
```

- **Lint** the "betterangels" application:

```
yarn nx lint betterangels
```

- **Test** the "betterangels" application:

```
nx test betterangels
```

### Versioning

- Production - x.y.z
- Development - x.y.z-beta.t

## Backend Development

The betterangels_backend is built on Django, a high-level Python web framework. It also utilizes Celery for distributed task processing, enabling the scheduling and execution of tasks.

### Starting Django

To start the Django backend server:

```bash
nx run betterangels-backend:start
```

Once started, you can access the Django development server at the default address: http://localhost:8000/ or the port you've configured.

### Starting the Celery Beat Scheduler

The scheduler, powered by Celery Beat, is responsible for triggering scheduled tasks. If you'd like to test the scheduled tasks, you will need to run the scheduler.

The scheduler is responsible for triggering scheduled tasks. If you'd like to test the scheduled tasks, you will need to run the scheduler.

To start the scheduler:

```bash
nx run betterangels-backend:start-scheduler
```

### Starting the Worker

Workers handle task execution. They can run without the scheduler if you're not testing scheduled tasks.

To start a worker:

```bash
nx run betterangels-backend:start-worker
```

Note: While workers can run independently of the scheduler, the scheduler requires at least one worker to process the scheduled tasks.

### Testing Emails

Django provides a flexible way to handle email backends. By default, our configuration uses the file-based email backend to capture sent emails as files. This is helpful for local development and testing without actually sending real emails.

#### Using the File-based Email Backend

Configure the .env File: Set the email backend in your .env file to use the file-based backend:

```bash
POST_OFFICE_EMAIL_BACKEND=django.core.mail.backends.filebased.EmailBackend
```

Checking Sent Emails: After configuring the backend, any email sent from the application will be stored as a file under tmp/app-emails in the project's directory.

Reading Emails: Navigate to the tmp/app-emails directory and open the email files to view the rendered HTML content. Each file represents an individual email sent from the application.

#### Switching to SES (Amazon Simple Email Service)

Before switching to SES, ensure that you're authenticated to AWS using Single Sign-On (SSO).

```bash
aws sso login
```

Configure the .env File: Update the email backend in your .env file to use the django_ses backend:

```bash
POST_OFFICE_EMAIL_BACKEND=django_ses.SESBackend
```

Sending & Receiving: With the above configuration, any emails sent from the application will now be dispatched through Amazon SES.