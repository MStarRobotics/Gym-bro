# Simple devcontainer Dockerfile for Python backend development
# Based on Microsoft's official Python devcontainer image
ARG VARIANT="3.11"
FROM mcr.microsoft.com/devcontainers/python:1-${VARIANT}

# Install prerequisites, Node for frontend tooling and Docker CLI for development convenience
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    git \
    gnupg \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    nodejs \
    npm \
    python3-venv \
    rsync \
    ssh && \
    unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    # Install Poetry
    curl -sSL https://install.python-poetry.org | python3 - && \
    echo "export PATH=\"$HOME/.local/bin:$PATH\"" >> /etc/profile.d/poetry_path.sh

# Add user-level npm location to PATH
ENV PATH="/home/vscode/.local/bin:/home/vscode/.yarn/bin:/home/vscode/.npm-global/bin:$PATH"

# Create a workspace /app folder
WORKDIR /workspace

# Install node version manager or tools as necessary (optional)

# Install Flutter SDK (stable channel)
RUN git clone https://github.com/flutter/flutter.git /usr/local/flutter -b stable && \
    chown -R root:root /usr/local/flutter && \
    /usr/local/flutter/bin/flutter --version || true

# Add Flutter to PATH for all users
ENV PATH="/usr/local/flutter/bin:/usr/local/flutter/bin/cache/dart-sdk/bin:$PATH"

# Default user is vscode in Microsoft devcontainers
USER vscode

# Install Android command line tools (sdkmanager) to /usr/local/android-sdk
RUN set -eux; ANDROID_SDK_ROOT=/usr/local/android-sdk; mkdir -p "$ANDROID_SDK_ROOT"
RUN curl -sSL https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -o /tmp/cmdline-tools.zip
RUN unzip /tmp/cmdline-tools.zip -d /usr/local/android-sdk
RUN mkdir -p /usr/local/android-sdk/cmdline-tools/latest
RUN mv /usr/local/android-sdk/cmdline-tools/* /usr/local/android-sdk/cmdline-tools/latest/ && rm /tmp/cmdline-tools.zip
RUN set -eux; ANDROID_SDK_ROOT=/usr/local/android-sdk; /usr/local/android-sdk/cmdline-tools/latest/bin/sdkmanager --sdk_root="$ANDROID_SDK_ROOT" \
        "platform-tools" \
        "platforms;android-33" \
        "build-tools;33.0.2" \
        "emulator" \
        "system-images;android-33;google_apis;x86_64" || true
RUN chown -R vscode:vscode /usr/local/android-sdk
RUN set -eux; ANDROID_SDK_ROOT=/usr/local/android-sdk; /usr/local/android-sdk/cmdline-tools/latest/bin/sdkmanager --licenses || true
RUN echo "no" | /usr/local/android-sdk/cmdline-tools/latest/bin/avdmanager create avd -n test -k "system-images;android-33;google_apis;x86_64" --device "pixel" || true

ENV ANDROID_HOME="/usr/local/android-sdk"
ENV ANDROID_SDK_ROOT="/usr/local/android-sdk"
ENV PATH="$PATH:/usr/local/android-sdk/platform-tools:/usr/local/android-sdk/cmdline-tools/latest/bin"
