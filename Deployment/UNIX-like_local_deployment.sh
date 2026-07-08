#!/usr/bin/bash
# Deploys a suitable local Python environment for UNIX-like operating systems.

# Path settings:
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
TARGET_DIR="$(dirname "$SCRIPT_DIR")/Requirements/Python"
PYTHON_TAR="$(dirname "$TARGET_DIR")/python-3.10.12.tgz"

# OS settings:
declare -a OS_PACKEGE_MANAGERS_COMMANDS=(
  # Debian|Ubuntu:
  "apt install -y"
  # Fedora|RHEL8+|Rocky|Alma:
  "dnf install -y"
  # CentOS|RHEL7:
  "yum install -y"
  # Arch|Manjaro:
  "pacman -Sy --noconfirm"
  # openSUSE:
  "zypper --non-interactive in"
  # Alpine:
  "apk add --no-cache"
  # FreeBSD:
  "pkg install -y"
  # macOS|Darvin:
  "brew install"
)

# Checks that the required version of Python is installed.
check_python_existence() {
  if ! python_version=$(python --version 2>&1 | awk '{print $2}')
  then
    if ! python_version=$(python3 --version 2>&1 | awk '{print $2}')
    then
      return 1
    fi

  if ! [[ "$python_version" == 3.10.* ]]
  then
    return 1
  fi

  return 0
  fi
}

# Installing packages required to build Python.
get_python_builder_packages() {
  for command_type in "${OS_PACKEGE_MANAGERS_COMMANDS[@]}"
      do
        echo -e "\e[43mTrying to install the packages needed to build Python from source...\e[0m"
        command $command_type \
          build-essential \
          libssl-dev \
          zlib1g-dev \
          libbz2-dev \
          libreadline-dev \
          libsqlite3-dev \
          libffi-dev \
          liblzma-dev \
          uuid-dev \
          libncursesw5-dev \
          libgdbm-dev libgdbm-compat-dev \
          tk-dev \
          libnsl-dev \
          libtirpc-dev \
          2>&1 | grep -v "command not found"
      done
}

# Deploy Python downloaded from the official website.
install_python() {
  echo -e "\e[36mDeploying Python.3.10.12...\e[0m"
  command "$TARGET_DIR/configure" \
    --prefix="$TARGET_DIR" \
    --enable-optimizations \
    --with-ensurepip=install

  make -j"$(nproc)"
  make -f "$TARGET_DIR/Makefile" \
    -C "$TARGET_DIR" install
}

# Download Python from the official website and unpack it.
get_python() {
  echo -e "\e[36mGetting Python.3.10.12 from the official website...\e[0m"
  curl -L -o "$PYTHON_TAR" \
    "https://www.python.org/ftp/python/3.10.12/python-3.10.12.tgz"

  tar -xzf "$PYTHON_TAR" \
    -С "$TARGET_DIR"
}

# Creates a virtual Python environment.
create_venv() {
  if ! python -m venv "$TARGET_DIR" 2>/dev/null
  then
    python3 -m venv "$TARGET_DIR"
  fi
}

# Checks sudo privileges, since without them it is impossible to execute the script.
check_sudo() {
  if [[ "$EUID" -ne 0 ]]
  then
    if [[ -z "$SUDO_USER" ]]
    then
    echo -e "\e[31mTo execute this instruction, you need sudo privilege...\e[0m"
    exit 1
    fi
  fi
}

execute() {
  check_sudo

  if ! ls "$TARGET_DIR"
  then
    mkdir -p "$TARGET_DIR"
  fi

  if check_python_existence
  then
    echo -e "\e[36mCreating a virtual environment from a local version of Python.3.10...\e[0m"
    if ! create_venv
    then
      for command_type in "${OS_PACKEGE_MANAGERS_COMMANDS[@]}"
      do
        echo -e "\e[43mpython3.10-venv was no found. Trying to install the python3.10-venv package...\e[0m"
        command $command_type "python3.10-venv" 2>&1 | grep -v "command not found"
      done
      if ! create_venv
      then
        echo -e "\e[31mAn error occurred during deployment...\e[0m"
        echo -e "\e[31mLooks like python3.10-venv failed to install...\e[0m"
        exit 1
      fi
    fi

  else
    if ! get_python
    then
      echo -e "\e[31mAn error occurred during deployment...\e[0m"
      echo -e "\e[31mUnable to download Python from the official website.\e[0m"
      exit 1
    fi

    if ! install_python
    then
      if ! get_python_builder_packages
      then
        echo -e "\e[31mAn error occurred during deployment...\e[0m"
        echo -e "\e[31mUnable to build downloaded version of Python...\e[0m"
        exit 1
      fi
    fi


    if ! comand "$TARGET_DIR" -m venv --copies "$TARGET_DIR" 2>/dev/null
    then
      if ! comand "$TARGET_DIR"/bin/python3 -m venv --copies "$TARGET_DIR"
      then
        echo -e "\e[31mAn error occurred during deployment...\e[0m"
        echo -e "\e[31mUnable to create virtual environment from downloaded version of Python...\e[0m"
        exit 1
      fi
    fi

  fi

  if ! comand "$TARGET_DIR"/bin/python3 \
      -m pip3 install \
      -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null
      then
        if ! comand "$TARGET_DIR"/bin/python3 \
        -m pip install \
        -r "$SCRIPT_DIR/requirements.txt"
        then
          echo -e "\e[31mAn error occurred during deployment...\e[0m"
          echo -e "\e[31mFailed to install Python libraries from requirements file.\e[0m"
          exit 1
        fi
      fi

  if ls "$PYTHON_TAR" 2>/dev/null
  then
    echo -e "\e[36mRemoving the installation python.exe file...\e[0m"
    rm "$PYTHON_TAR"
  fi

  echo -e "\e[32mThe creation of a Python virtual environment has been successful!\e[0m"
  echo -e "\e[32mLocation: $TARGET_DIR\e[0m"
}

execute